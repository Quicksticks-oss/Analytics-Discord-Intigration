import discord
import base64
import json
client = discord.Client(intents=discord.Intents.all())
TOKEN = ''

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.__contains__('88Analytics88'):
        message = message.content.replace('88Analytics88', '')
        message = json.loads(base64.b85decode(message).decode())
        print(message)

client.run(TOKEN)
