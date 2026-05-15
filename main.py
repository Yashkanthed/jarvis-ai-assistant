"""
╔══════════════════════════════════════════════════════════╗
║         J.A.R.V.I.S — AI Voice Assistant                ║
║         Built by: [Your Name]                           ║
║         Original idea: CodeWithHarry                    ║
║         Enhanced & Modified: Full Laptop Control        ║
╚══════════════════════════════════════════════════════════╝

FEATURES:
  ✅ Say "Jarvis" to START, "Jarvis stop" to STOP
  ✅ Google search by voice — "search Python tutorial on Google"
  ✅ Maths by voice — "what is 25 times 4" → Jarvis says answer
  ✅ Conversational AI — remembers what you said (like ChatGPT!)
  ✅ Volume control, screenshots, keyboard shortcuts
  ✅ Open websites and apps
  ✅ Weather, news, jokes, Wikipedia, time, date, reminders
  ✅ Full laptop control (shutdown, restart, lock, sleep)

INSTALL:
  pip install -r requirements.txt

RUN:
  python main.py
  → Say "Jarvis" to wake up
  → Say "Jarvis stop" to sleep
"""

# ─────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from groq import Groq
from gtts import gTTS
import pygame
import os
import datetime
import pyjokes
import wikipedia
import subprocess
import time
import pyautogui
import math        # used for safe math evaluation


# ─────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────
GROQ_API_KEY    = "your_groq_key_here"
NEWS_API_KEY    = "your_newsapi_key_here"
WEATHER_API_KEY = "your_weather_key_here"  # free at openweathermap.org
DEFAULT_CITY    = "Indore"   # change to your city

engine    = pyttsx3.init()
reminders = []

# ── CONVERSATION HISTORY ──────────────────────────────────
# Stores full chat so Jarvis REMEMBERS context — just like ChatGPT!
# Every message = {"role": "user" or "assistant", "content": "text"}
# We send ALL previous messages to Groq so it knows the whole conversation.
import json

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read().strip()
                if not content:       # file is empty → return fresh list
                    return []
                return json.loads(content)
        except:
            return []             # file is corrupted → return fresh list
    return []

def save_memory(history):
    """Save memory to file so it persists across restarts."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

conversation_history = load_memory()


# ═════════════════════════════════════════════════════════
# SECTION 1 — SPEAK
# ═════════════════════════════════════════════════════════

def speak(text):
    global stop_speaking
    stop_speaking = False
    print(f"[JARVIS]: {text}")   # ← make sure this line is there!

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
# ═════════════════════════════════════════════════════════
# SECTION 2 — AI BRAIN  (with conversation memory!)
# ═════════════════════════════════════════════════════════

def aiProcess(command):
    """
    Sends command to Groq AI with FULL conversation history.

    WHY conversation_history?
    Without it → Jarvis forgets everything after each reply (like a goldfish!)
    With it    → Jarvis remembers the whole conversation (like ChatGPT!)

    Example:
      You:    "My name is Rahul"
      Jarvis: "Nice to meet you Rahul!"
      You:    "What is my name?"
      Jarvis: "Your name is Rahul!"   ← it remembered!

    HOW IT WORKS:
      1. Add user message to history
      2. Send entire history to Groq
      3. Get reply
      4. Add Jarvis reply to history too
      5. Next time — history has both sides of conversation
    """
    global conversation_history

    # Add user's message to history
    conversation_history.append({
        "role": "user",
        "content": command
    })

    # Keep history to last 20 messages (10 exchanges)
    # Prevents the API request from getting too large
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a smart, friendly, and conversational AI assistant — "
                    "just like Tony Stark's Jarvis. You run on the user's laptop in India. "
                    "Be warm, witty, and helpful. Remember everything the user tells you in this conversation. "
                    "Give detailed answers when the user asks something interesting, "
                    "but keep it short for simple tasks. "
                    "Never say you are an AI model — you are Jarvis, a personal assistant."
                )
            }
        ] + conversation_history   # send full history every time!
    )

    reply = completion.choices[0].message.content

    # Add Jarvis reply to history
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    # Save to file immediately after every reply
    save_memory(conversation_history)

    return reply


# ═════════════════════════════════════════════════════════
# SECTION 3 — GOOGLE SEARCH  (NEW!)
# ═════════════════════════════════════════════════════════

def search_google(command):
    """
    Searches Google for whatever the user says.

    HOW IT EXTRACTS THE QUERY:
      "search Python tutorial on Google" → removes "search" and "on google"
      "Google search machine learning"   → removes "google search"
      "search what is AI"                → removes "search"
      → remaining text becomes the search query

    webbrowser.open() opens the Google search results page directly.
    The query is URL-encoded using .replace(" ", "+") for the URL.
    """
    c = command.lower()

    # Remove all trigger phrases to get the pure search query
    for phrase in ["search on google", "on google", "google search", "search for", "search"]:
        c = c.replace(phrase, "")

    query = c.strip()

    if query:
        speak(f"Searching Google for {query}.")
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        speak("What should I search for?")


# ═════════════════════════════════════════════════════════
# SECTION 4 — MATHS CALCULATOR  (NEW!)
# ═════════════════════════════════════════════════════════

def calculate(command):
    """
    Solves math problems spoken by voice.

    HOW IT WORKS:
      1. Convert spoken words to math symbols
         "25 times 4"   → "25 * 4"
         "10 plus 5"    → "10 + 5"
         "20 minus 8"   → "20 - 8"
         "100 divided by 4" → "100 / 4"
         "5 squared"    → "5 ** 2"
         "square root of 16" → "math.sqrt(16)"

      2. Use Python's eval() to compute the expression
         eval("25 * 4") → 100

      WHY eval() with allowed names?
         Raw eval() is dangerous — a user could type harmful code.
         We pass allowed_names={"math": math} so ONLY math functions work.
         Nothing else can be executed — it's safe!

    Examples:
      "what is 25 times 4"         → "25 times 4 equals 100"
      "calculate 100 divided by 5" → "100 divided by 5 equals 20"
      "square root of 144"         → "square root of 144 equals 12"
      "2 to the power of 10"       → "2 to the power of 10 equals 1024"
    """
    c = command.lower()

    # Remove question words to get just the math part
    for word in ["what is", "calculate", "compute", "solve", "tell me", "how much is"]:
        c = c.replace(word, "")

    original = c.strip()   # save original spoken version for the reply

    # Convert spoken words → math symbols
    c = c.replace("times",          "*")
    c = c.replace("multiplied by",  "*")
    c = c.replace("multiply",       "*")
    c = c.replace("plus",           "+")
    c = c.replace("add",            "+")
    c = c.replace("minus",          "-")
    c = c.replace("subtract",       "-")
    c = c.replace("divided by",     "/")
    c = c.replace("divide by",      "/")
    c = c.replace("divided",        "/")
    c = c.replace("to the power of","**")
    c = c.replace("squared",        "** 2")
    c = c.replace("cubed",          "** 3")
    c = c.replace("square root of", "math.sqrt")
    c = c.replace("percent of",     "* 0.01 *")

    c = c.strip()

    try:
        # Safe eval — only allows math functions, nothing else
        result = eval(c, {"__builtins__": {}}, {"math": math})

        # Clean up result — show integer if no decimal part
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        answer = f"{original} equals {result}"
        speak(answer)

    except Exception:
        # If eval fails → ask AI to solve it instead
        speak("Let me think about that.")
        ai_answer = aiProcess(f"Solve this math problem and give only the answer: {original}")
        speak(ai_answer)


# ═════════════════════════════════════════════════════════
# SECTION 5 — OTHER FEATURES
# ═════════════════════════════════════════════════════════

def tell_time():
    return f"It is {datetime.datetime.now().strftime('%I:%M %p')}"

def tell_date():
    return f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}"

def get_weather(city=DEFAULT_CITY):
    try:
        url  = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        return f"Weather in {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}."
    except:
        return "Couldn't fetch weather right now."

def get_news():
    try:
        articles = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        ).json().get('articles', [])[:5]
        speak("Here are the top headlines.")
        for i, a in enumerate(articles, 1):
            speak(f"{i}. {a['title']}")
    except:
        speak("Couldn't fetch news right now.")

def tell_joke():
    return pyjokes.get_joke()

def search_wikipedia(query):
    try:
        q = query.lower()
        for w in ["wikipedia","search","who is","what is","tell me about"]:
            q = q.replace(w, "")
        return wikipedia.summary(q.strip(), sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results. Did you mean: {', '.join(e.options[:3])}?"
    except:
        return "Couldn't find that on Wikipedia."

def add_reminder(command):
    text = command.lower().replace("remind me to", "").strip()
    if text:
        reminders.append(text)
        return f"Reminder set: {text}"
    return "What should I remind you about?"

def list_reminders():
    if not reminders:
        return "You have no reminders."
    return "Your reminders: " + ", ".join(f"{i+1}. {r}" for i,r in enumerate(reminders))

def control_volume(command):
    c = command.lower()
    if "mute" in c and "un" not in c: pyautogui.press("volumemute"); speak("Muted.")
    elif "unmute" in c: pyautogui.press("volumemute"); speak("Unmuted.")
    elif any(w in c for w in ["up","increase","high","louder"]):
        for _ in range(10): pyautogui.press("volumeup")
        speak("Volume increased.")
    elif any(w in c for w in ["down","decrease","low","quiet","lower"]):
        for _ in range(10): pyautogui.press("volumedown")
        speak("Volume decreased.")
    elif any(w in c for w in ["max","maximum","full"]):
        for _ in range(50): pyautogui.press("volumeup")
        speak("Volume at maximum.")
    elif any(w in c for w in ["minimum","very low"]):
        for _ in range(50): pyautogui.press("volumedown")
        speak("Volume at minimum.")
    else: speak("Volume command not understood.")

def take_screenshot():
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{ts}.png")
    pyautogui.screenshot(path)
    speak("Screenshot saved to Desktop.")

def type_text(command):
    text = command.lower().replace("type", "").strip()
    if text:
        speak(f"Typing: {text}")
        time.sleep(1)
        pyautogui.typewrite(text, interval=0.05)
    else:
        speak("What should I type?")

def keyboard_shortcut(command):
    c = command.lower()
    shortcuts = {
        "copy":("ctrl","c"),        "paste":("ctrl","v"),
        "cut":("ctrl","x"),         "undo":("ctrl","z"),
        "redo":("ctrl","y"),        "select all":("ctrl","a"),
        "save":("ctrl","s"),        "new tab":("ctrl","t"),
        "close tab":("ctrl","w"),   "new window":("ctrl","n"),
        "find":("ctrl","f"),        "zoom in":("ctrl","="),
        "zoom out":("ctrl","-"),    "refresh":("f5",),
        "full screen":("f11",),     "task manager":("ctrl","shift","esc"),
        "show desktop":("win","d"), "minimize":("win","down"),
        "maximize":("win","up"),    "alt tab":("alt","tab"),
        "go back":("alt","left"),   "go forward":("alt","right"),
        "switch tab":("ctrl","tab"),
    }
    for name, keys in shortcuts.items():
        if name in c:
            pyautogui.hotkey(*keys)
            speak(f"Done.")
            return
    speak("Shortcut not recognized.")

def open_application(command):
    c = command.lower()
    apps = {
        "notepad":"notepad.exe",         "calculator":"calc.exe",
        "paint":"mspaint.exe",           "file explorer":"explorer.exe",
        "task manager":"taskmgr.exe",    "cmd":"cmd.exe",
        "command prompt":"cmd.exe",      "settings":"ms-settings:",
        "vs code":"code",                "visual studio":"code",
        "chrome":"chrome",
        "brave":r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "word":"winword",                "excel":"excel",
        "powerpoint":"powerpnt",
    }
    for name, cmd in apps.items():
        if name in c:
            speak(f"Opening {name}.")
            subprocess.Popen(cmd, shell=True)
            return
    speak("I don't know that application.")

def system_control(command):
    c = command.lower()
    if "shutdown"      in c: speak("Shutting down in 5 seconds."); os.system("shutdown /s /t 5")
    elif "restart"     in c or "reboot" in c: speak("Restarting in 5 seconds."); os.system("shutdown /r /t 5")
    elif "sleep"       in c or "hibernate" in c: speak("Going to sleep."); os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif "lock"        in c: speak("Locking screen."); os.system("rundll32.exe user32.dll,LockWorkStation")
    elif "cancel"      in c: speak("Shutdown cancelled."); os.system("shutdown /a")
    else: speak("System command not understood.")

def close_window(command):
    if "tab" in command.lower(): pyautogui.hotkey("ctrl","w"); speak("Tab closed.")
    else: pyautogui.hotkey("alt","f4"); speak("Window closed.")


# ═════════════════════════════════════════════════════════
# SECTION 6 — COMMAND ROUTER
# ═════════════════════════════════════════════════════════

def processCommand(c):
    """
    Routes every command to the right function.
    Order matters — most specific checks first, AI last.
    """
    c_lower = c.lower().strip()

    # ── GOOGLE SEARCH ─────────────────────────────────────
    # Check FIRST before other "open" commands
    if "search" in c_lower or "google search" in c_lower:
        search_google(c)
        return

    # ── WEBSITES ──────────────────────────────────────────
    websites = {
        "open google"   :"https://google.com",
        "open youtube"  :"https://youtube.com",
        "open facebook" :"https://facebook.com",
        "open linkedin" :"https://linkedin.com",
        "open github"   :"https://github.com",
        "open instagram":"https://instagram.com",
        "open whatsapp" :"https://web.whatsapp.com",
        "open twitter"  :"https://twitter.com",
        "open netflix"  :"https://netflix.com",
        "open amazon"   :"https://amazon.in",
        "open chatgpt"  :"https://chat.openai.com",
        "open gmail"    :"https://mail.google.com",
        "open maps"     :"https://maps.google.com",
    }
    for phrase, url in websites.items():
        if phrase in c_lower:
            webbrowser.open(url); speak(f"Opening {phrase.replace('open ','')}.")
            time.sleep(1); return

    # ── MUSIC ─────────────────────────────────────────────
    if c_lower.startswith("play"):
        song = c_lower.split(" ",1)[1]
        link = musicLibrary.music.get(song)
        if link: speak(f"Playing {song}."); webbrowser.open(link)
        else: speak("Song not found in library.")
        return

    # ── MATHS ─────────────────────────────────────────────
    # Triggers on: "what is 5 times 3", "calculate 100/5",
    # "25 plus 10", "square root of 64", etc.
    math_triggers = ["calculate","times","divided by","multiplied",
                     "square root","plus","minus","squared","cubed",
                     "to the power","percent of","how much is"]
    is_math = any(t in c_lower for t in math_triggers)

    # Also check if command has numbers + operation words
    has_numbers = any(char.isdigit() for char in c_lower)

    if is_math and has_numbers:
        calculate(c)
        return

    # ── TIME & DATE ───────────────────────────────────────
    if "time"   in c_lower: speak(tell_time()); return
    if "date"   in c_lower or "day" in c_lower: speak(tell_date()); return

    # ── WEATHER ───────────────────────────────────────────
    if "weather" in c_lower:
        city = c_lower.split("in",1)[1].strip() if "in" in c_lower else DEFAULT_CITY
        speak(get_weather(city)); return

    # ── NEWS ──────────────────────────────────────────────
    if "news" in c_lower: get_news(); return

    # ── JOKES ─────────────────────────────────────────────
    if "joke" in c_lower: speak(tell_joke()); return

    # ── WIKIPEDIA ─────────────────────────────────────────
    if any(w in c_lower for w in ["wikipedia","who is","tell me about"]):
        speak(search_wikipedia(c)); return

    # ── REMINDERS ─────────────────────────────────────────
    if "remind me"  in c_lower: speak(add_reminder(c)); return
    if "reminders"  in c_lower: speak(list_reminders()); return

    # ── VOLUME ────────────────────────────────────────────
    if "volume" in c_lower or "mute" in c_lower or "unmute" in c_lower:
        control_volume(c); return

    # ── SCREENSHOT ────────────────────────────────────────
    if "screenshot" in c_lower: take_screenshot(); return

    # ── TYPE BY VOICE ─────────────────────────────────────
    if c_lower.startswith("type"): type_text(c); return

    # ── KEYBOARD SHORTCUTS ────────────────────────────────
    shortcut_words = ["copy","paste","cut","undo","redo","select all","save",
                      "new tab","close tab","new window","find","zoom in","zoom out",
                      "refresh","full screen","task manager","show desktop",
                      "minimize","maximize","alt tab","go back","go forward","switch tab"]
    if any(kw in c_lower for kw in shortcut_words): keyboard_shortcut(c); return

    # ── CLOSE ─────────────────────────────────────────────
    if "close" in c_lower: close_window(c); return

    # ── SYSTEM POWER ──────────────────────────────────────
    if any(w in c_lower for w in ["shutdown","restart","reboot","sleep","hibernate","lock"]):
        system_control(c); return

    # ── OPEN APPS ─────────────────────────────────────────
    if "open" in c_lower: open_application(c); return

    # ── GOODBYE ───────────────────────────────────────────
    if any(w in c_lower for w in ["bye","goodbye","exit","quit"]):
        speak("Goodbye! Have a great day."); exit()

    # ── FALLBACK → GROQ AI (with memory!) ─────────────────
    # Nothing matched → send to Groq AI
    # This now remembers the full conversation!
    output = aiProcess(c)
    speak(output)


# ═════════════════════════════════════════════════════════
# SECTION 7 — MAIN LOOP
# Say "Jarvis" to START, "Jarvis stop" to STOP
# ═════════════════════════════════════════════════════════

if __name__ == "__main__":
    speak("Jarvis is ready. Say Jarvis to activate me.")
    print("=" * 55)
    print("  Say 'Jarvis'      → to START listening")
    print("  Say 'Jarvis stop' → to STOP listening")
    print("  Say 'stop'        → to interrupt mid-speech")
    print("  Say 'bye'         → to exit completely")
    print("=" * 55)

    active = False

    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.3)

                if active:
                    print("\n[Listening for command...]")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                else:
                    # Only print sleeping message once, not continuously
                    print("\n[Sleeping... say 'Jarvis' to wake me]")
                    audio = r.listen(source, timeout=5, phrase_time_limit=2)

            command = r.recognize_google(audio)
            print(f"[Heard]: {command}")

            # WAKE UP
            if not active and "jarvis" in command.lower():
                active = True
                speak("Ya, I am listening.")

            # STOP
            elif active and "jarvis stop" in command.lower():
                active = False
                speak("Going to sleep. Say Jarvis to wake me up.")

            # PROCESS COMMAND
            elif active:
                processCommand(command)
                time.sleep(0.5)

        except sr.WaitTimeoutError:
            # Add small sleep here so it doesn't print continuously
            time.sleep(0.5)

        except sr.UnknownValueError:
            pass

        except Exception as e:
            print(f"[Error]: {e}")