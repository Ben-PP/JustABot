from pickle import TRUE
import discord

#TODO: Change the descriptions to be read from a file
#This happens when user sends message '!help'.
async def help(message):
    content = {
        "title":"Need help?",
        "description":"Here are all the commands that I know! Starting with commands that **everyone** can access.",
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
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)
    content = {
        "title":"Trust worthy?",
        "description":"These commands can be accessed roles with access level of **trusted** or above.",
        "fields": [
            {
                "name":"None",
                "value":"No trusted commands yet :("
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)
    content = {
        "title":"Power trip?",
        "description":"These commands can be trusted only in wise hands! To use these commands, role must have access level set to **admin**.",
        "fields": [
            {
                "name":"!roles",
                "value":"Used to for managing roles.",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

#!roles help
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
                "value":"Removes reaction from message and connection to a role.\n'!roles remove :emoji:'",
                "inline":True
            },
            {
                "name":"messages",
                "value":"Gives a list of messages that have reaction role or roles.",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

#!embed help
async def help_embed(message):
    content = {
        "title":"Embed",
        "description":"With this you can send embedded message.\n!embed\nSyntax for content is:\n{\n\"title\":\"Your title\",\n\"description\":\"Your description\",\n\"fields\": [\n{\n\"name\":\"Field name\",\n\"value\":\"Field value\",\n\"inline\":True\n}\n]\n}",
        "fields":[
            {
                "name":"Fields",
                "value":"You can add multiple field\nby separating each fiel block with ','\ninside the [] block."
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

#!access help
async def help_access(message):
    content = {
        "title":"Access",
        "description":"With this you can manage access levels needed to access certain features.\n**Levels are:** admin and trusted",
        "fields":[
            {
                "name":"add",
                "value":"Adds access level to a role.\n'!access add @role admin'",
                "inline": True
            },
            {
                "name":"remove",
                "value":"Removes access level from role.\n'!access remove @role'",
                "inline": True
            },
            {
                "name":"list",
                "value":"Lists all the roles that have access level set.",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)