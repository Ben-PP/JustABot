import help

#Everything related to role creating with the bot.
class Roles:
    active_message = None
    active_channel = None

    #Default method called when user writes message that starts with '!roles'.
    #Here the message is also split and searched for further commands.
    async def roles(message, client):

        message_splitted = message.content.split(" ")
        if len(message_splitted) <= 1 or message_splitted[1] == "help":
            await help.help_roles(message)
            return

        if message_splitted[1] == "add":
            await Roles.add_role(message, client)
            return
        
        if message_splitted[1] == "message":
            await Roles.set_message(message, int(message_splitted[2]))
            return

        if message_splitted[1] == "channel":
            await Roles.set_channel(message)
    
    #Adds reaction to specified message and connects a role to it
    #TODO: Needs delete_role
    async def add_role(message, client):

        if Roles.active_message == None:
            await message.channel.send("No message is set as active!")
            return
        if Roles.active_channel == None:
            await message.channel.send("No channel has been set!")
            return
        
        await Roles.active_message.add_reaction("🐱")
        #TODO: Finish the saving of reaction-role connection

    #Sets the active_message which is used for checking the reactions
    async def set_message(message, id):
        if Roles.active_channel == None:
            await message.channel.send("No channel has been set. Set channel first with '**!role channel #channelname!**'")
            return
        msg =  await Roles.active_channel.fetch_message(id)
        Roles.active_message = msg
        await message.channel.send("Active message has been set to: " + str(id))

    #Sets the active_channel to where the bot reacts
    async def set_channel(message):
        ch = message.channel_mentions
        Roles.active_channel = ch[0]
        await message.channel.send("Channel has been set to: <#"+str(Roles.active_channel.id)+">")

