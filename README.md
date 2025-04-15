# Threads-Bot

A simple bot that automatically posts AI-generated content to Threads.

## What it does

- Logs into your Threads account 
- Generates text using AI (gpt-4o-mini)
- Posts the content to your Threads account

## Setup

1. Install requirements:
   ```
   pip install selenium python-dotenv g4f
   ```

2. Create a `.env` file with:
   ```
   THREADS_USERNAME=your_username
   THREADS_PASSWORD=your_password
   PROMPT=Your prompt for AI to generate content
   ```

3. You also need Chrome browser installed.

## Running the bot

Simply run:
```
python app.py
```

Or use the .plist file to schedule automatic runs.

## Customization

Edit the PROMPTS list in `app.py` to change what kind of content the bot generates.
