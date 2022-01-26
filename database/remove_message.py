import sqlite3

def remove_message(guild_id, message_id):
    dbname = "databases/"+str(guild_id)+".db"
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    
    #Check and remove any reaction role related data on the message
    cursor.execute("SELECT * FROM reaction_role_messages WHERE message_id='"+str(message_id)+"'")
    message = cursor.fetchone()    
    if message != None:
        cursor.execute("DELETE FROM reaction_role_messages WHERE message_id='"+str(message_id)+"'")
        cursor.execute("DROP TABLE '"+str(message_id)+"'")
    #Check and remove any embed related data on the message
    #FIXME: check embedded database

    db.commit()
    db.close()