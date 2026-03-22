# 🤖 Telegram Jira Answerer (FastAPI + MCP)

Simple and powerful Telegram bot built with **FastAPI**, **Aiogram 3**, and **Model Context Protocol (MCP)** to interact with **Jira Cloud**. 
The bot uses **GPT-4o** (OpenAI SDK) to dynamically answer questions by fetching tools from a Jira MCP server.

## 🚀 Features
- **Smart Jira Access:** Ask "What are my open bugs?" or "Summarize project X" in natural language.
- **MCP Integration:** Uses `@aashari/mcp-server-atlassian-jira` for stable, headless Jira interaction.
- **Real-time Tools:** GPT-4o decides which Jira tools to call (search, create, update, etc.) on the fly.
- **FastAPI Lifespan:** Handles MCP server lifecycle automatically on startup/shutdown.

## 🛠️ Requirements
- **Python 3.10+**
- **Node.js** (to run the Jira MCP server)
- **Telegram Bot Token** (@BotFather)
- **OpenAI API Key**
- **Jira Credentials** (Site URL, Email, API Token)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd tg-jira-answerer
   ```

2. **Setup Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Install MCP Server locally:**
   ```bash
   npm install @aashari/mcp-server-atlassian-jira
   ```

4. **Configuration:**
   Rename `.env.example` to `.env` and fill in your keys:
   ```ini
   TELEGRAM_TOKEN=...
   OPENAI_API_KEY=...
   JIRA_URL=https://your-site.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-token
   ```

## 🏃 Running the Application

```bash
python -m uvicorn main:app --reload
```

## 📂 Project Structure
- `main.py`: Core application logic (FastAPI + Aiogram + MCP Client).
- `.env`: Secret keys and configuration (ignored by git).
- `node_modules/`: Local installation of the Jira MCP server.

## 📄 License
MIT
