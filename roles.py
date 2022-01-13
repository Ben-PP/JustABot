import discord
import help

#Everything related to role creating with the bot.
class Roles:

    #Default method called when user writes message that starts with '!roles'.
    #Here the message is also split and searched for further commands.
    async def roles(message):

        message_splitted = message.content.split(" ")
        if len(message_splitted) <= 1 or message_splitted[1] == "help":
            await help.help_roles(message)
            return
    
    #TODO: Roolien valinta viestiin reagoimalla
    def set_message(id):
        pass