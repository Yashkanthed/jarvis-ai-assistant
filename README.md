# 🤖 J.A.R.V.I.S — AI Voice Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Groq-Llama3-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Platform-Windows-lightblue?style=for-the-badge&logo=windows"/>
</p>

> **Just A Rather Very Intelligent System**  
> A fully voice-controlled AI assistant for Windows built in Python.  
> Inspired by Tony Stark's Jarvis — talks like ChatGPT, controls your laptop, and never forgets you!

---

## 🎥 How It Works

```
Say "Jarvis"        →   Jarvis wakes up and says "Ya, I am listening"
Say your command    →   Jarvis executes it instantly
Say "stop"          →   Jarvis stops talking mid-sentence
Say "Jarvis stop"   →   Jarvis goes back to sleep
Say "bye"           →   Jarvis exits
```

---

## ✨ Features

### 🧠 AI & Conversation
- Talks naturally like ChatGPT using **Groq AI (Llama 3)** — completely FREE
- **Permanent memory** — remembers your name, city, preferences forever
- Full conversation context — remembers what you said earlier in the chat

### 🌐 Web & Search
- **Google search by voice** — "search Python tutorial"
- Opens 13 websites — YouTube, Instagram, GitHub, Netflix, Gmail and more

### 💻 Laptop Control
- **Volume control** — "volume up", "mute", "volume max"
- **Screenshots** — "take a screenshot" → saves to Desktop
- **Type by voice** — "type hello world"
- **Keyboard shortcuts** — "copy", "paste", "undo", "save", "new tab" and more
- **Open apps** — Notepad, Calculator, VS Code, Chrome, Paint and more
- **System control** — "shutdown", "restart", "sleep", "lock"

### 📱 Information
- 🌤️ **Weather** — "weather in Mumbai"
- 📰 **News** — reads top 5 Indian headlines
- 😂 **Jokes** — "tell me a joke"
- 📖 **Wikipedia** — "who is Elon Musk"
- ⏰ **Time & Date** — "what time is it"
- 📝 **Reminders** — "remind me to drink water"
- 🧮 **Maths** — "what is 25 times 4", "square root of 144"
- 🎵 **Music** — "play skyfall" → opens on YouTube

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Yashkanthed/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### 2. Install all libraries
```bash
pip install -r requirements.txt
```

### 3. Get your FREE API keys
| Service | Link | Free? |
|---|---|---|
| Groq (AI brain) | console.groq.com | ✅ 100% Free |
| NewsAPI | newsapi.org | ✅ Free tier |
| OpenWeatherMap | openweathermap.org | ✅ Free tier |

### 4. Add your API keys in `main.py`
```python
GROQ_API_KEY    = "your_groq_key"
NEWS_API_KEY    = "your_newsapi_key"
WEATHER_API_KEY = "your_weather_key"
DEFAULT_CITY    = "Your City"
```

### 5. Run Jarvis!
```bash
python main.py
```

---

## 🗣️ Voice Commands

| Category | Say This |
|---|---|
| **Wake up** | "Jarvis" |
| **Sleep** | "Jarvis stop" |
| **Interrupt** | "stop" (while Jarvis is talking) |
| **Search** | "search machine learning on Google" |
| **Websites** | "open youtube" / "open instagram" |
| **Music** | "play skyfall" |
| **Maths** | "what is 144 divided by 12" |
| **Weather** | "weather in Delhi" |
| **News** | "news" |
| **Joke** | "tell me a joke" |
| **Wikipedia** | "who is APJ Abdul Kalam" |
| **Time** | "what time is it" |
| **Screenshot** | "take a screenshot" |
| **Volume** | "volume up" / "mute" / "volume max" |
| **Shortcuts** | "copy" / "paste" / "undo" / "save" |
| **Open apps** | "open notepad" / "open calculator" |
| **System** | "shutdown" / "restart" / "lock" |
| **Reminder** | "remind me to call mom" |
| **Chat** | Anything else → Groq AI answers! |

---

## 📁 Project Structure

```
jarvis-ai-assistant/
│
├── main.py           ← Main Jarvis program (run this!)
├── musicLibrary.py   ← Song name → YouTube URL dictionary
├── client.py         ← Groq API test file
├── requirements.txt  ← All pip packages
├── .gitignore        ← Files excluded from GitHub
└── README.md         ← This file
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| Groq API (Llama 3) | AI brain — free conversations |
| SpeechRecognition | Voice to text |
| gTTS + pygame | Text to speech |
| pyttsx3 | Offline TTS backup |
| pyautogui | Keyboard & mouse control |
| requests | Weather & news APIs |
| wikipedia | Wikipedia search |
| pyjokes | Random jokes |
| json | Permanent memory storage |

---

## 💡 How Memory Works

Jarvis saves your conversation to `jarvis_memory.json` locally on your PC.
Every time Jarvis starts, it loads this file so it remembers everything you told it before.

```
You:    "My name is Yash"           → saved to jarvis_memory.json
You:    "I am from Bhopal"          → saved to jarvis_memory.json
--- next day after restart ---
You:    "What is my name?"
Jarvis: "Your name is Yash!"  ✅
```

> Your data stays **100% on your laptop** — never sent to any server!

---

## 📚 Original Project Credit

Based on the Jarvis project by [CodeWithHarry](https://github.com/CodeWithHarry).  
Enhanced with 15+ new features including permanent memory, laptop control, Google search, maths, interrupt support, and conversational AI.

---

## 👨‍💻 Built by Yash Kanthed

⭐ Star this repo if you found it useful!
