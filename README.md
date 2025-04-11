# 🎮 Google's Pokémon Catching Game Auto-Catcher

![Auto-catches all 151 original Pokémon from Google's search game](https://github.com/kr4k0n/Google-Pokemon-Catching-Game-Auto-Catcher/blob/main/autopoke.gif?raw=true)

## Youtube Overview
[![Watch the video](https://i.ytimg.com/vi/hGYC34AgO5w/sddefault.jpg)](https://youtu.be/hGYC34AgO5w?si=mAAsvsDq38hGZd2v)


## ✨ Features
- 🤖 Auto-catches all 151 original Pokémon from Google's search game
- 📁 Progress tracking with JSON save file
- 🎯 Multiple search attempt strategies for each Pokémon
- 🏆 Automatic Master Ball claiming
- 📱 Mobile browser emulation for consistent experience
- ⚡ Graceful interruption handling (Ctrl+C)

## 🚀 Operation
1. Searches each Pokémon on Google
2. Clicks the Pokéball to catch
3. Handles success/failure cases
4. Automatically closes popups
5. Saves progress after each catch

## ⚙️ Setup Instructions
1. Install requirements:
   ```bash
   pip install playwright python-dotenv
   playwright install
   ```
2. Configure `.env` file with:
   ```
   BRAVE_PATH="/path/to/brave"
   ```
3. Run script:
   ```bash
   python gopoke.py
   ```
4. You can make the script to run headless (without showing the browser)
   by changing the value
   ```
   headless=False
   ```
   to
   ```
   headless=True
   ```
   in `gopoke.py`

## 🏆 Key Improvements
- 🛡️ Virtual environment validation
- 🎛️ Configurable rate limiting
- 📶 Better timeout handling
- 🔄 Retry mechanism for failed attempts
- 📊 Persistent progress tracking
- 🖥️ Browser automation optimizations

## 🔄 Key Changes
- Added explicit Chrome channel specification
- Improved error handling and logging
- Mobile-first emulation approach
- Animation delay handling
- Master Ball detection

## 🚨 Troubleshooting Tips
1. If game doesn't load:
   - ✅ Enable "Search Personalization" in Google settings
   - 🖥️ Keep browser window focused
   - 🚫 Don't move mouse during operation
2. Clear `progress.json` to reset catcher
3. Running in virtual environment is required
4. Ensure Brave/Chrome is properly installed

## ⚠️ Important Notes
 submissions-🐍 Requires Python 3.6+
- 🔄 Works with Google's original 151 Pokémon only
- ⏱️ Includes intentional UABrowser locking
- 🚫 Not affiliated with Google or Nintendo
- 📜 Credit original author (Phr34kz - Myself)
