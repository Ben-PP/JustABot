import sqlite3

def remove_message(guild_id, message_id):
    dbname = "databases/"+str(guild_id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    
    #Check and remove any reaction role related data on the message.
    cursor.execute("SELECT * FROM reaction_role_messages WHERE message_id='"+str(message_id)+"'")
    message = cursor.fetchone()    
    if message != None:
        cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(message_id)+"'")
        cursor.execute("DROP TABLE '"+str(message_id)+"'")

    #Check and remove any data in embedded_messages.
    cursor.execute("SELECT * FROM embedded_messages WHERE embed_message_id='"+str(message_id)+"'or sent_message_id='"+str(message_id)+"'")
    embed = cursor.fetchone()
    if embed != None:
        #Deletes the embedded message if it does not have reaction roles.
        cursor.execute("SELECT * FROM reaction_role_messages")
        if len(cursor.fetchall()) < 1:
            cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(embed[0])+"'")
        #Deletes the message from which the embed was sent.
        cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(embed[2])+"'")
    cursor.execute("DELETE FROM embedded_messages WHERE embed_message_id='"+str(message_id)+"'or sent_message_id='"+str(message_id)+"'")

    #Remove data from used_messages.
    cursor.execute("DELETE FROM used_messages WHERE message_id='"+str(message_id)+"'")

    db.commit()
    db.close()