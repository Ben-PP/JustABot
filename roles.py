from distutils import command
import re
import help

#Everything related to role creating with the bot.
class Roles:
    active_message = None
    active_channel = None
    reaction_role = dict()

    #TODO: When Python 3.10 available, replace message_splitted with match-case and make arguments into class attributes
    #Default method called when user writes message that starts with '!roles'.
    #Here the message is also split and searched for further commands.
    async def roles(message, client):

        message_splitted = message.content.split(" ")

        if len(message_splitted) <= 1 or message_splitted[1] == "help":
            await help.help_roles(message)
        elif message_splitted[1] == "add":
            await Roles.add_reactionrole(message, message_splitted)
        elif message_splitted[1] == "remove":
            await Roles.remove_reactionrole(message, message_splitted)
        elif message_splitted[1] == "message":
            if len(message_splitted) < 3 or not(message_splitted[2].isdecimal()):
                await message.channel.send("No message id was found on the message!")
                return
            await Roles.set_message(message, int(message_splitted[2]))
        elif message_splitted[1] == "channel":
            await Roles.set_channel(message)
        else:
            await message.channel.send("Unknown command '**"+message_splitted[1]+"**'.\nType '**!roles help**' for more commands.")
            

    #Adds reaction to specified message and connects a role to it.
    async def add_reactionrole(message, message_splitted):

        if Roles.active_message == None:
            await message.channel.send("No message is set as active!")
            return
        if len(message_splitted) < 4:
            await message.channel.send("Not enough arguments on the message!\nYou must firs provide an emoji, and after that provide the role!")
            return
        if re.search("^<@&.*>$", message_splitted[3]) == None:
            await message.channel.send("No role was found from the message. use @ to mention the role!")
            return

        used_emoji = message_splitted[2]
        role_id = int(message_splitted[3][3:(len(message_splitted[3])-1)])
        message_id = str(Roles.active_message.id)
        

        if not(message_id in Roles.reaction_role):
            Roles.reaction_role[message_id] = dict()
            Roles.reaction_role[message_id][used_emoji] = role_id
            try:
                await Roles.active_message.add_reaction(used_emoji)
            except:
                await message.channel.send("No such emoji found!")
                Roles.reaction_role[message_id].pop(used_emoji)
                Roles.reaction_role.pop(message_id)
                return
            await message.channel.send("Role has been added to "+used_emoji, reference=Roles.active_message)
            return
        if not(used_emoji in Roles.reaction_role[message_id]):
            Roles.reaction_role[message_id][used_emoji] = role_id
            try:
                await Roles.active_message.add_reaction(used_emoji)
            except:
                await message.channel.send("No such emoji found!")
                Roles.reaction_role[message_id].pop(used_emoji)
                return
            await message.channel.send("Role has been added to "+used_emoji, reference=Roles.active_message)
            return

        await message.channel.send("This reaction allready has a role attached to it. Please choose another reaction or delete the old one.")
    
    #Deletes reaction from message and removes the connection to a role.
    async def remove_reactionrole(message, message_splitted):
        if Roles.active_message == None:
            await message.channel.send("No message is set as active!")
            return

        used_emoji = message_splitted[2]
        message_id = str(Roles.active_message.id)

        if not(message_id in Roles.reaction_role):
            await message.channel.send("No reaction found from currently active message!")
            return
        if not(used_emoji in Roles.reaction_role[message_id]):
            await message.channel.send("No such reaction found from the message!")
            return
        
        Roles.reaction_role[message_id].pop(used_emoji)
        await Roles.active_message.clear_reaction(used_emoji)


    #Sets the active_message which is used for checking the reactions.
    async def set_message(message, message_id):
        if Roles.active_channel == None:
            await message.channel.send("No channel has been set. Set channel first with '**!role channel #channelname!**'")
            return
        msg = None
        try:
            msg =  await Roles.active_channel.fetch_message(message_id)
        except:
            await message.channel.send("No messages were found with the id: "+str(message_id))
            return
        Roles.active_message = msg
        await message.channel.send("Active message has been set to: " + str(message_id))


    #Sets the active_channel to where the bot reacts.
    async def set_channel(message):
        ch = message.channel_mentions
        if len(ch) < 1:
            await message.channel.send("No channel mentioned on the message!")
            return
        Roles.active_channel = ch[0]
        await message.channel.send("Channel has been set to: <#"+str(Roles.active_channel.id)+">")

    #Sets correct role for user according to with what he reacted.
    async def set_role(payload,client):

        message_id = str(payload.message_id)
        used_emoji = str(payload.emoji)
        guild = client.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if not(message_id in Roles.reaction_role):
            return
        if not(used_emoji in Roles.reaction_role[message_id]):
            return
        await user.add_roles(guild.get_role(Roles.reaction_role[message_id][used_emoji]))

    #Removes correct role from the user according to with what he reacted.
    async def remove_role(payload, client):
        message_id = str(payload.message_id)
        used_emoji = str(payload.emoji)
        guild = client.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if not(message_id in Roles.reaction_role):
            return
        if not(used_emoji in Roles.reaction_role[message_id]):
            return
        await user.remove_roles(guild.get_role(Roles.reaction_role[message_id][used_emoji]))