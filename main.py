import discord
import os
import requests
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def getEyepopPipelineUrl():
    url = "https://api.eyepop.ai/api/v1/user/pops/100/config"
    token = os.getenv('EYEPOP_TOKEN')

    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': 'application/json'
    }
    
    response = requests.request("GET", url, headers=headers)
    

    return response.json()['url'] + '/pipelines/' + response.json()['pipeline_id'] + '/source'


def setEyepopSource(endpoint, url):
    payload = json.dumps({
        "sourceType": "URL",
        "url": url
    })
    headers = {
    'Content-Type': 'application/json'
    }
    params = {
        'mode': 'preempt',
        'processing': 'sync'
    }
    response = requests.request("PATCH", endpoint, headers=headers, data=payload, params=params)
    print (response.text)
    return response.json()
    
pipelineUrl = getEyepopPipelineUrl()
class EyebotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
        print(message)
        if message.author == self.user:
            return
        if len(message.attachments):
            for attachment in message.attachments:
                if (attachment.content_type[:5] == 'image'):
                    # pipelineUrl = getEyepopPipelineUrl()
                    objects = setEyepopSource(pipelineUrl, attachment.url)
                    isHotdog = False
                    for obj in objects['objects']:
                        if obj['classLabel'] == 'hot dog':
                            isHotdog = True
                            await message.channel.send('Hot dog! 🌭')
                            return;
                    await message.channel.send('Not hot dog! 🚫🌭')
                    

intents = discord.Intents.default()
intents.message_content = True

client = EyebotClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))
