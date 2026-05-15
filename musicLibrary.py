"""
musicLibrary.py
================
A simple dictionary that maps song names → YouTube URLs.

WHY A DICTIONARY?
  - O(1) lookup speed — instant search no matter how many songs
  - Easy to add new songs: just add a new key-value pair
  - Key   = what you SAY  (lowercase, so matching works easily)
  - Value = YouTube link  (what Jarvis opens in the browser)

HOW TO ADD A SONG:
  1. Go to YouTube and copy the video URL
  2. Add it below: "song name": "youtube url"
  3. Say "play song name" to Jarvis

NOTE: song names must be lowercase to match the voice recognition output
"""

music = {
    # ── Original songs ──────────────────────────────
    "stealth" : "https://www.youtube.com/watch?v=U47Tr9BB_wE",
    "march"   : "https://www.youtube.com/watch?v=Xqeq4b5u_Xw",
    "skyfall" : "https://www.youtube.com/watch?v=DeumyOzKqgI",
    "wolf"    : "https://www.youtube.com/watch?v=ThCH0U6aJpU",

    # ── Add your own songs below ─────────────────────
    "shape of you"    : "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "believer"        : "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "blinding lights" : "https://www.youtube.com/watch?v=4NRXx6U8ABQ",
    "stay"            : "https://www.youtube.com/watch?v=kTJczUoc26U",
    "levitating"      : "https://www.youtube.com/watch?v=TlNUHcLAa_0",
}