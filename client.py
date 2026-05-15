"""
client.py — OpenAI API Test File
==================================
This is a STANDALONE test file to verify your OpenAI API key works
before integrating it into main.py.

Run this file first. If you see a response → your key is working!

HOW THE OPENAI API WORKS:
─────────────────────────
1. You send a list of 'messages' (like a chat history)
2. Each message has a 'role':
      'system' → sets the AI's personality/behavior
      'user'   → what the human says
      'assistant' → what the AI previously said (for multi-turn chats)
3. The API returns a 'completion' object
4. The actual text reply is at: completion.choices[0].message.content

WHY choices[0]?
  The API can return multiple alternative answers (called 'choices').
  By default it returns 1. We always take index [0] (the first one).
"""

from groq import Groq

# Replace with your actual key from console.groq.com (FREE!)
client = Groq(api_key="GROK_API_KEY")

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # FREE Llama 3 model on Groq
    messages=[
        {
            "role": "system",
            "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud"
        },
        {
            "role": "user",
            "content": "what is coding"
        }
    ]
)

# Print the AI's reply
print(completion.choices[0].message.content)