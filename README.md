WhisperMod: Discord Voice Message Moderator
======================

Functionality
-----

This bot listens for audio messages sent in a Discord server's text channels. When it detects an audio message, it:

1.  Writes the audio file attachment to a memory stream
2.  Converts from OGG to WAV format (required by OpenAI)
3.  Sends the WAV-converted stream to OpenAI's Whisper API for transcription
4.  Checks the text transcription for appropriateness using OpenAI's Content Moderation API
5.  Deletes the message and warns the user if it violates content policy

Technical Approach
------------------

*   Used the Discord.py API wrapper to connect to Discord and listen for events
*   Handled asynchronous events and API calls using asyncio
*   Manipulated audio files using ffmpeg and pydub
*   Made API calls to OpenAI's Whisper and Content Moderation APIs
*   Developed custom functions for transcribing, content checking, and moderating

### Architecture

The bot follows an event-driven architecture using Discord's API. The main entry point is the `on_message` event handler which detects new messages. This passes the message to the `process_voice_message` function to handle audio files. Supporting functions like `transcribe_voice_message` and `content_check` make the OpenAI API calls. `process_voice_message` uses `asyncio.create_task()` so it can process messages concurrently.

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
    * Migrating to bytesio
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

If using GitHub Actions to push to Azure Container Instances:
- Read the following article for context:
  - [Configure a GitHub Action to create a container instance](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action?tabs=userlevel)

- You'll need some repository secrets set up:
  - AZURE_CREDENTIALS
  - REGISTRY_LOGIN_SERVER
  - REGISTRY_USERNAME
  - REGISTRY_PASSWORD
  - RESOURCE_GROUP
  - OPENAI_API_KEY
  - DISCORD_SECRET_KEY
  - LOG_ANALYTICS_WORKSPACE_ID
  - LOG_ANALYTICS_WORKSPACE_KEY
 
- Note that my workflows/main.yml is based on [Azure's ACI Deploy sample](https://github.com/Azure/aci-deploy)

Privacy and Legal
---------------
If you plan to use this bot, it is critically important to notify your Discord server's users that their audio messages will be sent to third-party AI services like OpenAI for processing. Get explicit opt-in consent from users before running the bot, as it will transmit their voice data outside of Discord without their knowledge otherwise.

Operate this bot in compliance with Discord's Terms of Service and Community Guidelines. You may need permission from Discord to use bots that process user data in servers.

You bear full responsibility for making sure this bot is used legally and ethically. Do not assume you have the rights to capture, transmit, or process users' audio messages without consent. Consult laws in your jurisdiction regarding data collection and bot usage.

Use human moderators whenever possible - do not rely solely on this bot for moderation. I provide no guarantees that this bot will operate flawlessly or accurately moderate content.

Disclaimer
---------------
I am not an attorney and provide no legal advice. I assume no liability for how you use this bot or any consequences from your use of it. Consult an attorney if you need legal guidance on complying with laws when operating this bot. Use and modify this bot at your own discretion - I am not liable for any outcomes related to your use of it.
