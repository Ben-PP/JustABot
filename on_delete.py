import os
import database.remove_message as remove_message
import database.remove_channel as remove_channel
import database.remove_role as remove_role


#Called when message is deleted
def message_deleted(payload):
    remove_message.remove_message(payload.guild_id, payload.message_id)

def channel_deleted(channel):
    remove_channel.remove_channel(channel.guild.id, channel.id)

def role_deleted(role):
    remove_role.remove_role(role)

def guild_deleted(guild):
    if os.path.exists("databases/"+guild.id+".db"):
        os.remove("databases/"+guild.id+".db")
