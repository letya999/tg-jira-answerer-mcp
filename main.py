import os
import json
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Setup AI & Telegram
bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
dp = Dispatcher()
llm = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Globals for MCP
mcp_session: ClientSession | None = None
mcp_stdio_context = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mcp_session, mcp_stdio_context

    logging.info("Initializing Jira MCP Client (using @aashari/mcp-server-atlassian-jira)...")
    
    # Map variables for @aashari/mcp-server-atlassian-jira
    jira_url = os.getenv("JIRA_URL", "")
    # Extract site name from https://site-name.atlassian.net
    site_name = ""
    if "atlassian.net" in jira_url:
        site_name = jira_url.split("://")[-1].split(".atlassian.net")[0]
    
    custom_env = os.environ.copy()
    if site_name:
        custom_env["ATLASSIAN_SITE_NAME"] = site_name
    custom_env["ATLASSIAN_USER_EMAIL"] = os.getenv("JIRA_EMAIL", "")
    custom_env["ATLASSIAN_API_TOKEN"] = os.getenv("JIRA_API_TOKEN", "")

    # Path to the locally installed server
    server_script = os.path.join(os.getcwd(), "node_modules", "@aashari", "mcp-server-atlassian-jira", "dist", "index.js")
    
    server_params = StdioServerParameters(
        command="node",
        args=[server_script],
        env=custom_env
    )

    try:
        mcp_stdio_context = stdio_client(server_params)
        mcp_read, mcp_write = await mcp_stdio_context.__aenter__()
        mcp_session = ClientSession(mcp_read, mcp_write)
        await mcp_session.__aenter__()
        await mcp_session.initialize()
        logging.info("MCP Client connection to Jira Initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize MCP Client: {e}")

    # Start Telegram Bot listening
    if bot:
        if WEBHOOK_URL:
            logging.info(f"Setting webhook URL to {WEBHOOK_URL}")
            await bot.set_webhook(WEBHOOK_URL)
        else:
            logging.info("Running standard long-polling in background.")
            await bot.delete_webhook(drop_pending_updates=True)
            asyncio.create_task(dp.start_polling(bot))

    yield

    logging.info("Shutting down...")
    if mcp_session:
        await mcp_session.__aexit__(None, None, None)
    if mcp_stdio_context:
        await mcp_stdio_context.__aexit__(None, None, None)
    if bot and WEBHOOK_URL:
        await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Endpoint for Telegram webhook updates.
    """
    if not bot:
        return {"error": "Bot not initialized"}
    
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "up", "mcp_connected": mcp_session is not None}

async def ask_jira(question: str) -> str:
    if not mcp_session:
        return "Not connected to Jira via MCP. Check logs for initialization errors."
    if not llm:
        return "OpenAI client is not configured."
    
    try:
        logging.info("Fetching available MCP tools from Jira...")
        response = await mcp_session.list_tools()
    except Exception as e:
        logging.error(f"MCP Session error (maybe connection closed): {e}")
        return f"Lost connection to Jira MCP: {e}. Please restart the application."
    
    openai_tools = []
    for tool in response.tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
        
    messages = [
        {"role": "system", "content": "You are a helpful assistant integrated with Jira via MCP. You can search issues, get tickets, comment, and read project details using provided tools. Answer in the same language as the user."},
        {"role": "user", "content": question}
    ]
    
    logging.info(f"Starting conversation with GPT for question: {question}")
    # Allow up to 10 tool call iterations
    for iteration in range(10):
        completion = await llm.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=openai_tools if openai_tools else None,
            tool_choice="auto" if openai_tools else "none"
        )
        msg = completion.choices[0].message
        
        # Convert Pydantic model to dictionary for appending to messages
        msg_dict = msg.model_dump(exclude_unset=True)
        # If content is None, we should set it to empty string or remove it
        # based on OpenAI API requirements (it should be present if no tool_calls)
        messages.append(msg_dict)
        
        if not msg.tool_calls:
            return msg.content if msg.content else "No content returned from model."
            
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args_str = tool_call.function.arguments
            logging.info(f"GPT calls MCP tool: {func_name} with args: {func_args_str}")
            
            try:
                func_args = json.loads(func_args_str)
                tool_result = await mcp_session.call_tool(func_name, arguments=func_args)
                result_texts = [c.text for c in tool_result.content if c.type == "text"]
                result_text = "\n".join(result_texts)
            except Exception as e:
                logging.error(f"Error calling MCP tool {func_name}: {e}")
                result_text = f"Error: {e}"
                
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": result_text if result_text else "Success"
            })
            
    return "Reached maximum iteration limit when interacting with tools."

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для общения с Jira через протокол MCP.\nЗадай мне любой вопрос (например: \"Найди мои последние открытые баги\").")

@dp.message()
async def process_question(message: types.Message):
    if not llm:
        await message.answer("Я не могу отвечать: не настроен OPENAI_API_KEY.")
        return
        
    processing_msg = await message.answer("Думаю и проверяю Jira...")
    try:
        reply = await ask_jira(message.text)
        await processing_msg.edit_text(reply, parse_mode=None)
    except Exception as e:
        logging.error(f"Error processing question: {e}", exc_info=True)
        await processing_msg.edit_text(f"Произошла ошибка: {e}")
