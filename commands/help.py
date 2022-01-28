import discord

#This happens when user sends message '!help'.
async def help(message):
    content = {
        "title":"Need help?",
        "description":"Here are all the commands that I know! Starting with commands that **everyone** can access.",
        "fields": [
            {
                "name":"help",
                "value":"You can add **'help'**\nto get more info\nabout any !command.",
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
                "name":"!embed",
                "value":"With this you can make me send an embedded message. To save embed, you have to have admin level.",
                "inline":True
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
            },
            {
                "name":"!access",
                "value":"This is used for giving access levels for roles.",
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
                "name":"list",
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
        "description":"With this you can send embedded message. You can send embed only once or you can save the embed so it can be edited later by editing the original message what was used to create the embed.",
        "fields":[
            {
                "name":"onetime",
                "value":"Sends embedded message without saving it. This can not be edited later.",
                "inline":True
            },
            {
                "name":"save",
                "value":"Admin level needed.\n**Only use this if needed!**\nSends embedded message. This can be edited later.",
                "inline":True
            },
            {
                "name":"list",
                "value":"Lists all the embedded messages that have been saved with their original messages.",
                "inline":True
            },
            {
                "name":"syntax",
                "value":"Show syntax for sending embeds.",
                "inline":True
            }
        ]
    }
    embed = discord.Embed.from_dict(content)
    await message.channel.send(embed=embed)

async def help_embed_syntax(message):
    description = """
        After the onetime/save you put your embed which has to be like this.\n
        (Without the ' at the start and the end and replace **bold** with your custom text.)\n
        '\{\n
        \"title\":\"**your title**\",\n\"description\":\"**something here**\",\n
        \"fields\":[\n
        \{\n
        \"name\":\"**name of the field**\",\n
        \"value\":\"**some thing for the field**\",\n
        \"inline\": **True**\n
        \}\n
        \]\n
        \}'
    """
    content = {
        "title":"How to embed?",
        "description":description,
        "fields":[
            {
                "name":"Inline",
                "value":"This **must** be either **True** or **False** and written exactly like that! This decides if the multiple fields are side by side or below each other.",
                "inline":True
            },
            {
                "name":"Fields",
                "value":"You are allowed to add more fields. Each field must be inside \{\} and separated by comma.",
                "inline":True
            },
            {
                "name":"Length",
                "value":"Discord limits maximum length of messages to 2000 characters. To maximize length, you can delete all spaces and line changes between brackets.",
                "inline":True
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