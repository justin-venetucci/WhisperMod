WhisperMod: Discord Voice Message Moderator
======================

About
-----

This bot listens for audio messages sent in a Discord server's text channels. When it detects an audio message, it:

1.  Downloads the audio file attachment
2.  Converts from OGG to WAV format (required by OpenAI)
3.  Sends the WAV file to OpenAI's Whisper API to transcribe to text
4.  Checks the text transcription using OpenAI's Content Moderation API
5.  Deletes the message if it violates content policy

I built this bot from scratch without using any boilerplate code or templates :)

Environment Setup
-----------------

*   Created and activated a virtual environment
*   Installed required libraries like Discord, OpenAI, and Pydub
*   Got API keys for OpenAI and Discord
*   Configured environment variables for semi-secure key management

Technical Approach
------------------

*   Used the Discord.py API wrapper to connect to Discord and listen for events
*   Handled asynchronous events and API calls using asyncio
*   Manipulated audio files using ffmpeg and pydub
*   Made API calls to OpenAI's Whisper and Content Moderation APIs
*   Developed custom functions for transcribing, content checking, and moderating
*   Followed best practices like environmnt variables and removing temporary files

### Architecture

The bot follows an event-driven architecture using Discord's API. The main entry point is the `on_message` event handler which detects new messages. This passes the message to the `process_voice_message` function to handle audio files. Supporting functions like `transcribe_voice_message` and `content_check` make the OpenAI API calls.

### Code Snippets

#### Discord message event handling

```python
@client.event
async def on_message(message):
    if message.author == client.user:  
        return
    print('Message received')
    await process_voice_message(message)
```

#### Transcribing audio using Whisper API

```python
async def transcribe_voice_message(file_path):
    transcript = openai.Audio.transcribe("whisper-1", open(file_path, "rb"))
    return transcript['text']
```

#### Content policy check using Content Moderation API
```python
async def content_check(text):
  response = openai.Moderation.create(
     input = text
  )
  is_flagged = response["results"][0]["flagged"]
  return is_flagged
```
Challenges
----------

*   Learning asynchronous programming in Python to properly handle Discord and API events
*   Finding the right audio manipulation libraries to convert between formats
    * It took me *forever* to get ffmpeg installed properly...
    * Turns out I just needed to relaunch VS Code ¯\\\_(ツ)_/¯
*   Passing audio files to OpenAI's API correctly
    * Creating and opening files
    * Working with io and asyncio
*   Handling errors and edge cases with audio messages
    * Settled on just console printing as the program runs to track failure points
*   Deleting messages and notifying users of violations

Future Work
-----------

*   Implementing user, role, or channel whitelisting and blacklisting
*   Adding persistent storage for transcripts and violations
*   Creating admin dashboard to configure moderation settings
*   Expanding moderation capabilities beyond audio messages
*   Using OpenAI's Chat Completion endpoint to provide more qualitative message analysis
    * Could be used to provide a more hollistic review of a message when combined with the quantitative Moderations AI
*   Get it working on an EC2 instance or in ﾟ✧. *containers* .✧ﾟ (is joke)
*   Storing keys in a key management system like Azure Key Vault (yes I know I just mixed AWS and Azure)

Running the Bot
---------------

To run this bot yourself:

1.  Clone the repository
2.  Configure your `.env` file with your API keys
    - OPENAI_API_KEY
    - DISCORD_SECRET_KEY
3.  Install dependencies with `pip install -r requirements.txt`
4.  Run `python bot.py`

If using Docker:

1.  Build the container using the dockerfile using "`docker build -t <choose an image name> .`"
2.  Run the container using "`docker run -it -e {env arguments} <image name from above>`"

Privacy and Legal
---------------
If you plan to use this bot, it is critically important to notify your Discord server's users that their audio messages will be sent to third-party AI services like OpenAI for processing. Get explicit opt-in consent from users before running the bot, as it will transmit their voice data outside of Discord without their knowledge otherwise.

Operate this bot in compliance with Discord's Terms of Service and Community Guidelines. You may need permission from Discord to use bots that process user data in servers.

You bear full responsibility for making sure this bot is used legally and ethically. Do not assume you have the rights to capture, transmit, or process users' audio messages without consent. Consult laws in your jurisdiction regarding data collection and bot usage.

Use human moderators whenever possible - do not rely solely on this bot for moderation. I provide no guarantees that this bot will operate flawlessly or accurately moderate content.

Disclaimer
---------------
I am not an attorney and provide no legal advice. I assume no liability for how you use this bot or any consequences from your use of it. Consult an attorney if you need legal guidance on complying with laws when operating this bot. Use and modify this bot at your own discretion - I am not liable for any outcomes related to your use of it.