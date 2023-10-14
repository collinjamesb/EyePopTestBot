import discord
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class EyebotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = EyebotClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))
