import sqlite3

def remove_message(payload):
    dbname = "databases/"+str(payload.guild_id)+".db"
    db = sqlite3.connect(dbname)
    db.execute("PRAGMA foreign_keys=ON")
    cursor = db.cursor()
    
    #Check and remove any reaction role related data on the message.
    cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(payload.message_id)+"'")

    #Check and remove any data in embedded_messages.
    cursor.execute("""DELETE FROM embedded_messages WHERE
        embed_message_id='"""+str(payload.message_id)+"""' OR
        sent_message_id='"""+str(payload.message_id)+"""'
    """)


    db.commit()
    db.close()