import discord
from decouple import config

client = discord.Client()
TOKEN = config('TOKEN')

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hello user!')
    
    if message.content.startswith('!How are you?'):
        await message.channel.send('I am fine thanks!')
    
client.run(TOKEN)