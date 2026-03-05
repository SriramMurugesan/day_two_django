# 🦙 Django Ollama Chatbot

A modern, feature-rich AI chatbot built with **Django** and **Ollama (Llama 3.2)**. Chat with a locally-running large language model through a sleek, dark-themed web interface — no API keys, no cloud, fully private.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Llama 3.2 Integration** | Powered by Ollama running locally — your data never leaves your machine |
| 💬 **Multi-Session Chat** | Create, switch, and delete separate conversations |
| 🧠 **Context-Aware** | Full conversation history sent with each request for contextual responses |
| 📝 **Markdown Rendering** | Assistant responses render with rich formatting (code blocks, lists, tables) |
| 🎨 **Premium Dark UI** | Glassmorphic design with smooth animations and gradient accents |
| 📱 **Responsive Layout** | Works seamlessly on desktop and mobile with collapsible sidebar |
| ⌨️ **Keyboard Shortcuts** | Enter to send, Shift+Enter for newlines |
| 💡 **Suggestion Cards** | Quick-start prompts for new conversations |
| ⚡ **Typing Indicator** | Animated dots while the model generates a response |
| 🗄️ **Persistent History** | All chats saved in SQLite — pick up where you left off |

---

## 🛠️ Prerequisites

Before you begin, make sure you have:

- **Python 3.10+** installed
- **Ollama** installed and running → [Install Ollama](https://ollama.com/download)
- **Llama 3.2** model pulled:
  ```bash
  ollama pull llama3.2
  ```

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/day_two_django.git
cd day_two_django
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
cd djangotutorial
python3 manage.py migrate
```

### 5. Start the Development Server

```bash
python3 manage.py runserver
```

### 6. Open the Chatbot

Navigate to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

> **Note:** Make sure Ollama is running (`ollama serve`) before sending messages.

---

## 📁 Project Structure

```
day_two_django/
├── requirements.txt
├── README.md
└── djangotutorial/
    ├── manage.py
    ├── db.sqlite3
    ├── mysite/                    # Django project configuration
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── chatbot/                   # 🦙 Chatbot application
        ├── apps.py                # App configuration
        ├── models.py              # ChatSession & Message models
        ├── views.py               # Chat views & Ollama API integration
        ├── urls.py                # URL routing
        ├── admin.py               # Django admin registration
        ├── migrations/            # Database migrations
        ├── templates/
        │   └── chatbot/
        │       └── chat.html      # Chat interface template
        └── static/
            └── chatbot/
                └── styles.css     # Premium dark theme stylesheet
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python) |
| **AI Model** | Llama 3.2 via Ollama |
| **Database** | SQLite |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Markdown** | marked.js (CDN) |
| **API** | Ollama REST API (`localhost:11434`) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/chatbot/` | Main chat interface |
| `POST` | `/chatbot/send/` | Send a message and get AI response |
| `GET` | `/chatbot/new/` | Create a new chat session |
| `GET` | `/chatbot/history/?session_id=<uuid>` | Get message history |
| `GET` | `/chatbot/sessions/` | List all chat sessions |
| `GET` | `/chatbot/session/<uuid>/` | Open a specific session |
| `POST` | `/chatbot/session/<uuid>/delete/` | Delete a session |

---

## ⚙️ Configuration

The Ollama connection settings are defined in `chatbot/views.py`:

```python
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"
```

To use a different model (e.g., `llama3.1`, `mistral`, `codellama`):

1. Pull the model: `ollama pull <model-name>`
2. Update `OLLAMA_MODEL` in `views.py`

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| **"Cannot connect to Ollama"** | Run `ollama serve` in a separate terminal |
| **"Model not found"** | Run `ollama pull llama3.2` |
| **Slow responses** | Normal for first request (model loading). Subsequent requests are faster |
| **Port conflict** | Change the Django port: `python3 manage.py runserver 8080` |
| **Module not found** | Ensure virtualenv is active and run `pip install -r requirements.txt` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using <strong>Django</strong> + <strong>Ollama</strong>
</p>