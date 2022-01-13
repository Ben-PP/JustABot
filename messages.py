import discord
import ast

import help

#Things to make the bot send messages
class Messages:

    #Sends an embedded message from user sent message
    async def embed(message):
        
        message_splitted = message.content.split(" ")
        if len(message_splitted) <= 1 or message_splitted[1] == "help":
            await help.help_embed(message)
            return

        message_no_command = message.content[-(len(message.content)-7):]
        print(message_no_command)
        content = ast.literal_eval(message_no_command)
        embed = discord.Embed.from_dict(content)
        await message.channel.send(embed=embed)