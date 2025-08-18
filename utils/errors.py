error_messages = {}  # {user_id: message_object}

async def send_error(channel, user, content):
    prev_msg = error_messages.get(user.id)
    if prev_msg:
        try:
            await prev_msg.delete()
        except:
            pass
    msg = await channel.send(f"{user.mention} {content}")
    error_messages[user.id] = msg
