from pickle import TRUE
import discord

#TODO: Change the descriptions to be read from a file
#This happens when user sends message '!help'.
async def help(message):
    content = {
        "title":"Need help?",
        "description":"Here are all the commands that I know!",
        "fields": [
            {
                "name":"!xxx help",
                "value":"You can add **'help'**\nto get more info\nabout it.",
                "inline":True
            },
            {
                "name":"!embed",
                "value":"With this you can make\nme send an embedded message.",
                "inline":True
            },
            {
                "name":"!roles",
                "value":"Used to for managing roles.",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

#Command specific help for !roles
async def help_roles(message):
    content ={
        "title":"Roles",
        "description":"You can use me to manage different roles on the server.\nPut these commands after !roles",
        "fields":[
            {
                "name":"set",
                "value":"Sets the channel and message as active.\n'!roles set #channel messageid'",
                "inline":True
            },
            {
                "name":"add",
                "value":"Adds reaction to message and connects a role to it which is assigned to everyone who reacts with it.\n'!roles add :emoji: @role'",
                "inline":True
            },
            {
                "name":"remove",
                "value":"Remoces reaction from message and connection to a role.\n'!roles remove :emoji:'",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

async def help_embed(message):
    content = {
        "title":"Embed",
        "description":"With this you can send embedded message.\nSyntax for content is:\n{\n\"title\":\"Your title\",\n\"description\":\"Your description\",\n\"fields\": [\n{\n\"name\":\"Field name\",\n\"value\":\"Field value\",\n\"inline\":True/False\n}\n]\n}",
        "fields":[
            {
                "name":"Fields",
                "value":"You can add multiple field\nby separating each fiel block with ','\ninside the [] block."
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)