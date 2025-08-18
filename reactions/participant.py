import discord
from utils.persistence import save_event
from utils.errors import send_error
from config import MAX_PARTICIPANTS
from datetime import datetime

async def handle_reaction_add(reaction, user, events, bot):
    if user.bot:
        return
    message = reaction.message
    # 対応する部屋
    for event_id, event in events.items():
        if event.get("message_id") == message.id:
            break
    else: return

    # 絵文字 → 時刻変換
    try:
        time_str = reaction.emoji
        if len(time_str) == 4 and time_str.isdigit():
            slot = f"{time_str[:2]}:{time_str[2:]}"
        else:
            await send_error(message.channel, user, "❌ 不正な時間リアクションです")
            return
    except:
        return

    # 他枠に参加済みかチェック
    for s, plist in event["participants"].items():
        if any(p["id"]==user.id for p in plist):
            await send_error(message.channel, user, "❌ 参加できる時間は1枠のみです（リアクションは1つまでしか押せません）")
            try: await reaction.remove(user)
            except: pass
            return

    # 参加者追加
    if slot not in event["participants"]:
        event["participants"][slot] = []
    event["participants"][slot].append({
        "id": user.id,
        "name": user.display_name,
        "url": f"https://discord.com/users/{user.id}",
        "waitlist": False
    })

    # 補欠処理
    plist = event["participants"][slot]
    if len(plist) > MAX_PARTICIPANTS:
        for p in plist[MAX_PARTICIPANTS:]:
            p["waitlist"] = True

    save_event(event_id, event)
    await update_participant_list(event_id, events, bot)

async def handle_reaction_remove(reaction, user, events, bot):
    if user.bot:
        return
    message = reaction.message
    for event_id, event in events.items():
        if event.get("message_id") == message.id:
            break
    else: return

    try:
        time_str = reaction.emoji
        if len(time_str) == 4 and time_str.isdigit():
            slot = f"{time_str[:2]}:{time_str[2:]}"
        else: return
    except:
        return

    # 参加者削除
    if slot in event["participants"]:
        event["participants"][slot] = [p for p in event["participants"][slot] if p["id"]!=user.id]
        # 補欠繰り上げ
        for p in event["participants"][slot]:
            if p.get("waitlist"):
                p["waitlist"] = False
                break

    save_event(event_id, event)
    await update_participant_list(event_id, events, bot)

async def update_participant_list(event_id, events, bot):
    event = events[event_id]
    channel = bot.get_channel(event["channel_id"])
    dt = datetime.fromisoformat(event["datetime"])
    month_day = dt.strftime("%m月%d日")
    hour_min = dt.strftime("%H:%M")
    content = f"@silent 🚨アモアス参加者一覧🚨\n部屋ID: {event_id}\n日時: {month_day} {hour_min}~\n\n"
    for slot in sorted(event["participants"].keys()):
        content += f"{slot}~\n"
        for p in event["participants"][slot]:
            name_link = f"[{p['name']}]({p['url']})"
            if p.get("waitlist"):
                name_link += "（補欠）"
            content += f"- {name_link}\n"
        content += "\n"

    list_msg_id = event.get("list_message_id")
    if list_msg_id:
        try:
            msg = await channel.fetch_message(list_msg_id)
            await msg.edit(content=content)
        except:
            msg = await channel.send(content)
            event["list_message_id"] = msg.id
    else:
        msg = await channel.send(content)
        event["list_message_id"] = msg.id

    save_event(event_id, event)
