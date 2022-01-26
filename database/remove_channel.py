import sqlite3

def remove_channel(guild_id, channel_id):
    dbname = "databases/"+str(guild_id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    #Check reaction role
    cursor.execute("SELECT * FROM reaction_role_messages WHERE channel_id='"+str(channel_id)+"'")
    messages = cursor.fetchall()
    for message in messages:
        cursor.execute("DROP TABLE '"+str(message[0])+"'")
        cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(message[0])+"'")

    #FIXME: check embed
    

    db.commit()
    db.close()