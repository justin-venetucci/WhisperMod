# Import libraries
import os
import io
#import base64
#import asyncio
import discord
import openai
import pydub
from dotenv import load_dotenv

# Get environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

linebreak = "--------------------------------------------"

# Create Discord client session
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Print login to console
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(linebreak)

#--------------------------------------------------------------------#
#                       Message Event Handler                        #
#--------------------------------------------------------------------#

# When a message is sent in a server that the bot is in
@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:  
        return
    
    print('Message received')
    await process_voice_message(message)
    print(linebreak)

#--------------------------------------------------------------------#
#                            Main Function                           #
#--------------------------------------------------------------------#

async def process_voice_message(message):
    # Check if the message has attachments
    if not message.attachments:
        # The message does not have attachments
        print("Message does not have attachment, ignoring")
        return
    
    # The message has attachments
    print("Message has attachment")

    # Retrieve the first message attachment
    attachment = message.attachments[0]

    # Check if attachment is voice message
    if not attachment.is_voice_message():
        # The message is not a voice message
        print('Attachment is not a voice message, ignoring')
        return

    # The attachment is a voice message
    print('Attachment is a voice message, getting content')

    # Get the voice message attachment
    audio_bytes_ogg = await attachment.read()
    print('Audio bytes gotten successfully')
    
    # Convert the ogg bytes to wav bytes
    audio_bytes_wav = pydub.AudioSegment.from_ogg(io.BytesIO(audio_bytes_ogg))
    print("Audio bytes converted to wav")

    # Create new wav file with wav bytes
    wav_file_path = "audio.wav"

    audio_bytes_wav.export(wav_file_path, format="wav")
    print("Wav file created")

    #-----------------------------------#
    #     Call Supporting Functions     #
    #-----------------------------------#

    # Transcribe the voice message
    transcript = await transcribe_voice_message(wav_file_path)
    print("Wav file transcribed")

    # Delete wav file
    os.remove(wav_file_path)
    print("Wav file deleted")

    # Print transcription
    print("----------------------")
    print(f"Transcript: {transcript}")
    print("-----------")

    # Perform content check on the transcript
    is_flagged = await content_check(transcript)
    print(f"Is Flagged: {is_flagged}")
    print("----------------------")
    # Take moderation actions if needed
    if is_flagged:
        await moderate_message(message)

#--------------------------------------------------------------------#
#                        Supporting Functions                        #
#--------------------------------------------------------------------#

async def transcribe_voice_message(file_path):
    """Passes a file path to OpenAI's Whisper model for transcription.\n
    Target file must be of type mp3, mp4, mpeg, mpga, m4a, wav, or webm"""

    transcript = openai.Audio.transcribe("whisper-1", open(file_path, "rb"))
    return transcript['text']

async def content_check(text):
    """Returns a boolean value of whether a given input violates OpenAI's content policy"""
    
    response = openai.Moderation.create(
    input = text
    )
    is_flagged = response["results"][0]["flagged"]
    return is_flagged

async def moderate_message(message):
        """Deletes a message. Will do more later."""
        await message.delete()
        print("**Message deleted**")
        await message.channel.send(f"Be nice, {message.author.mention}")

# Run the script
client.run(os.getenv('DISCORD_SECRET_KEY'))