# 🤖 Telegram Jira Answerer (FastAPI + MCP)

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 🌍 English Version

Simple and powerful Telegram bot built with **FastAPI**, **Aiogram 3**, and **Model Context Protocol (MCP)** to interact with **Jira Cloud**. 
The bot uses **GPT-4o** (OpenAI SDK) to dynamically answer questions by fetching tools from a Jira MCP server.

### 🚀 Features
- **Smart Jira Access:** Ask "What are my open bugs?" or "Summarize project X" in natural language.
- **MCP Integration:** Uses `@aashari/mcp-server-atlassian-jira` for stable, headless Jira interaction.
- **Real-time Tools:** GPT-4o decides which Jira tools to call (search, create, update, etc.) on the fly.
- **FastAPI Lifespan:** Handles MCP server lifecycle automatically on startup/shutdown.

### 🛠️ Requirements
- **Python 3.10+**
- **Node.js** (to run the Jira MCP server)
- **Telegram Bot Token** (@BotFather)
- **OpenAI API Key**
- **Jira Credentials** (Site URL, Email, API Token)

### 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/letya999/tg-jira-answerer-mcp.git
   cd tg-jira-answerer-mcp
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

---

<a name="russian"></a>
## 🇷🇺 Русская версия

Простой и мощный Telegram-бот, построенный на **FastAPI**, **Aiogram 3** и **Model Context Protocol (MCP)** для взаимодействия с **Jira Cloud**.
Бот использует **GPT-4o** (OpenAI SDK), чтобы динамически отвечать на вопросы, получая инструменты от MCP-сервера Jira.

### 🚀 Возможности
- **Умный доступ к Jira:** Спрашивайте "Какие у меня открытые баги?" или "Сделай саммари проекта X" на естественном языке.
- **Интеграция MCP:** Использует `@aashari/mcp-server-atlassian-jira` для стабильного взаимодействия с Jira без браузера.
- **Инструменты в реальном времени:** GPT-4o самостоятельно решает, какие инструменты Jira вызывать (поиск, создание, обновление и т.д.) на лету.
- **FastAPI Lifespan:** Автоматически управляет жизненным циклом MCP-сервера при запуске и остановке.

### 🛠️ Требования
- **Python 3.10+**
- **Node.js** (для запуска MCP-сервера Jira)
- **Telegram Bot Token** (@BotFather)
- **OpenAI API Key**
- **Данные Jira** (URL сайта, Email, API-токен)

### 📦 Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/letya999/tg-jira-answerer-mcp.git
   cd tg-jira-answerer-mcp
   ```

2. **Настройте Python окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   pip install -r requirements.txt
   ```

3. **Установите MCP-сервер локально:**
   ```bash
   npm install @aashari/mcp-server-atlassian-jira
   ```

4. **Конфигурация:**
   Переименуйте `.env.example` в `.env` и заполните ключи:
   ```ini
   TELEGRAM_TOKEN=...
   OPENAI_API_KEY=...
   JIRA_URL=https://your-site.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-token
   ```

## 📄 License | Лицензия
MIT
