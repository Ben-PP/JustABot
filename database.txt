Each guild(Discord server) gets its own .db file

In the .db file there will always bee following tables:
    'active_messages'

'active_messages'
name    |   active_channel_id   | active_message_id
'roles' |   discordchannelid    | discordmessageid      #This is created when '!roles set' is sent succesfully.
'embeds'|   discordchannelid    | discordmessageid      #this is created when '!embed channel' is sent succesfully.

Following tables are added as needed:
	'(thiswillbemessageid)'	#Messageid is set on numbers for example '04944938387340903'
    'embedded_messages'     #This stores message that created the embed and the embed that was created.
	
'(thiswillbemessageid)'
emoji	|	role_id	
🔥	    |	discordroleid		#emoji needs to be unicode emoji

'embedded_messages'
request_message_id  |   sent_message_id
discordmessageid    |   discordmessageid