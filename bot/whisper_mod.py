import os
import io
import discord
import openai
import pydub
import asyncio
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create Discord client session
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Print login to console
@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')

# Message Event Handler
@client.event
async def on_message(message):
    if message.author == client.user:  
        return
    logger.debug('Message received')
    await asyncio.create_task(process_voice_message(message))

# Main Function
async def process_voice_message(message):
    # Catch if not voice message
    if not message.attachments or not message.attachments[0].is_voice_message():
        logger.debug('Message is not voice message, ignoring')
        return
    
    # If voice message
    logger.info('----------------------')
    logger.info('Voice message received')

    # Set attachment
    attachment_url = message.attachments[0]
    logger.debug(f'Voice file link: {attachment_url}')
    
    # Define file names
    filename = f'voice_message_{message.id}'
    filename_ogg = f'{filename}.ogg'
    filename_mp3 = f'{filename}.mp3'

    # Get attachment content, save to buffer
    buffer_ogg = io.BytesIO(await attachment_url.read())
    buffer_ogg.name = filename_ogg
    logger.debug('Attachment content captured to buffer')

    # Create PyDub AudioSegment from attachment
    audio_segment = pydub.AudioSegment.from_ogg(buffer_ogg)
    logger.debug('Audio segment created')
    
    # Create empty buffer to export AudioSegment to
    buffer_mp3 = io.BytesIO()
    buffer_mp3.name = filename_mp3 # for OpenAI
    logger.debug('Empty buffer created for mp3')

    # Export AudioSegment to buffer
    audio_segment.export(buffer_mp3, format="mp3")
    logger.debug('Segment converted to mp3')

    # Transcribe file with Whisper
    transcript = openai.Audio.transcribe("whisper-1", buffer_mp3)['text']
    #transcript = transcript_response['text']
    logger.debug('Voice message transcribed')

    # Log transcript
    logger.info(f'Transcript: {transcript}')

    # Pass to moderation model
    mod_response = openai.Moderation.create(input=transcript)
    logger.debug(mod_response)

    # Select flagged status only
    is_flagged = mod_response['results'][0]['flagged']
    logger.info(f'Is Flagged: {is_flagged}')

    if is_flagged:
        await message.delete()
        logger.info('Message deleted')
        await message.channel.send(f'I removed that voice message for containing offensive content. Be nice, {message.author.mention}')

# Run the script
client.run(os.getenv('DISCORD_SECRET_KEY'))