Each guild(Discord server) gets its own .db file

In the .db file there will always bee following tables:
    'active_messages'           ({name}, active_channel_id, active_message_id)
    'reaction_role_messages'    ({message_id}, channel_id)
    'embedded_messages'         ({embed_message_id}, embed_channel_id, sent_message_id, sent_channel_id)
    'access_level'              ({role_id}, is_admin,is_trusted)
    'used_messages'             ({message_id}, channel_id, in_table, is_table)

'active_messages'
name    |   active_channel_id   | active_message_id
'roles' |   discordchannelid    | discordmessageid      #This is created with '!roles set'

Following tables are added as needed:
	'(thiswillbemessageid)'	    ({emoji},role_id,channel_id)
    
	

'(thiswillbemessageid)'
emoji(bolb) |	role_id(integer)    |   channel_id(integer)
🔥	        |	discordroleid       |   discordchannelid        #emoji needs to be unicode emoji