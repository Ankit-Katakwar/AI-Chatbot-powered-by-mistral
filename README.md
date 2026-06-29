# 🎭 PersonaVerse

> **One Model. Multiple Minds.**

PersonaVerse is a multi-personality AI chatbot built using **LangChain**, **Mistral AI**, and **Streamlit**.

Instead of creating multiple AI models, PersonaVerse dynamically changes the behavior of a single language model by injecting different system prompts. Each personality has its own tone, response style, visual identity, and conversation behavior.

---

## ✨ Features

- 🎭 Multiple AI personalities
- 🤖 Powered by Mistral AI
- 🧠 LangChain message management
- 💬 Persistent chat history
- 🎨 Beautiful Streamlit UI
- ⚡ Cached model loading
- 🔄 Instant personality switching
- 📱 Responsive interface
- 🧹 Automatic conversation reset when switching personalities

---

## 🎭 Available Personalities

- 😏 Sarcastic AI
- 🔥 Angry AI
- 🌧️ Sad AI
- 🎭 Funny AI
- 📚 Teacher AI
- 🚀 Motivational AI
- 🌿 Concise AI

Each personality has its own:

- System Prompt
- Response Style
- Color Theme
- Icon
- Tagline

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- python-dotenv

---

## 📂 Project Structure

```
PersonaVerse
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone <repo-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
MISTRAL_API_KEY=YOUR_API_KEY
```

Run

```bash
streamlit run app.py
```

---

## 🧠 How It Works

Instead of training different models, PersonaVerse uses a different **System Prompt** for each personality.

```
User
      │
      ▼
Select Personality
      │
      ▼
System Prompt
      │
      ▼
Mistral AI
      │
      ▼
AI Response
```

Whenever the user switches personalities, the previous conversation is cleared and a fresh system prompt is injected to ensure consistent behavior.

---

## 💡 Future Improvements

- Voice conversations
- Memory support
- Custom personalities
- Image understanding
- Tool calling
- Multi-agent support
- Local LLM support

---

## 📸 Preview



---

## 📜 License

MIT License
