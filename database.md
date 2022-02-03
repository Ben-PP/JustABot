Each guild(Discord server) gets its own .db file

In the .db file there will always bee following tables:
    'active_messages'           ({name}, active_channel_id, active_message_id)

    'guild_roles'               ({role_id})

    'guild_channels'            ({channel_id})

    'access_level'              ({role_id}, is_admin,is_trusted)

    'reaction_role_messages'    ({message_id, emoji}, channel_id, role_id)

    'embedded_messages'         ({embed_message_id}, embed_channel_id, sent_message_id, sent_channel_id)

    'favorite_restaurants'      ({user_id, restaurant_name})