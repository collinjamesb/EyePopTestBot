import discord
from discord import app_commands
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

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.id}!')

@client.event
async def on_message(message):
        # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
        print(message)
        if message.author == client.user.id:
            return
        if len(message.attachments):
            for attachment in message.attachments:
                if (attachment.content_type[:5] == 'image'):
                    objects = setEyepopSource(pipelineUrl, attachment.url)
                    # Begin writing message to send (based on number of objects)
                    if ('objects' in objects):
                        obj_message = "This image contains a"
                        # Determine if 'a' or 'an'
                        fl = objects['objects'][0]['classLabel'][:1].lower() # First Letter
                        if (fl == 'a' or fl == 'e' or fl == 'i' or fl == 'o' or fl == 'u'):
                            obj_message += 'n'
                        obj_message += ' '
                    else:
                        obj_message = "There are no objects in this image"
                        await message.channel.send(obj_message)
                        return;
                    ii = 1
                    for obj in objects['objects']:
                        # Determine when to end the message
                        if ii == len(objects['objects']) and len(objects['objects']) > 1:
                            obj_message += "and " + obj['classLabel']
                        else:
                            obj_message += obj['classLabel']
                            # Oxdford commas are ok but no commas if there are only two objects
                            if len(objects['objects']) > 2:
                                obj_message += ","
                            obj_message += " "
                        ii += 1
                    await message.channel.send(obj_message)

@tree.command(name="hotdog", description="Jian Yang's hotdog detector", guild=discord.Object(id=1162845016532713653))
async def hotdog(interaction: discord.Interaction, image: discord.Attachment):
    print(image)
    await interaction.response.send_message("command")
                

client.run(os.getenv('DISCORD_TOKEN'))
