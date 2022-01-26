import discord
import ast

import commands.help as help

#FIXME: Make the messages sent modifiable
#Things to make the bot send messages

#Sends an embedded message from user sent message
async def embed(message):
    
    message_splitted = message.content.split(" ")
    if len(message_splitted) <= 1 or message_splitted[1] == "help":
        await help.help_embed(message)
        return
    elif message_splitted[1] == "onetime":
        await send_one_time(message, message_splitted)
        return
    elif message_splitted[1] == "save":
        await send_and_save(message, message_splitted)
        return

async def send_and_save(message, message_splitted):
    pass #CONTINUE:

async def send_one_time(message, message_splitted):
    if len(message_splitted) <= 4:
        await message.channel.send("Incorrect ammount of arguments. For help '**!embed help**'")
        return
    channels = message.channel_mentions
    if len(channels) < 1:
        await message.channel.send("No channel mentioned. Remember to **#mention** the channel.")
        return
    channel = channels[0]
    cut_letters = len(message_splitted[0]) + len(message_splitted[1]) + len(message_splitted[2]) + 3
    message_no_command = message.content[-(len(message.content)-cut_letters):]
    sent_message = await send(message_no_command, channel)
    if sent_message == None:
        await message.channel.send("Failed to send embed. Check syntax.")
    else:
        if message.channel != sent_message.channel:
            await message.channel.send("Embed sent! "+sent_message.jump_url)

#Sends the embedded message to correct channel.
#Returns Message that was sent or if message can't be sent,
#returns None
async def send(content, channel):
    print(content)
    try:
        content_out = ast.literal_eval(content)
    except:
        return None
    embed = discord.Embed.from_dict(content_out)
    try:
        return await channel.send(embed=embed)
    except:
        return None