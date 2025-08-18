from discord import app_commands
from datetime import datetime, timedelta
from utils.persistence import save_event, list_events_by_date
from utils.errors import send_error
from config import MAX_PARTICIPANTS


def register_create_command(bot, events):
    @bot.tree.command(name="createwolf", description="アモアス募集を作成")
    @app_commands.describe(date="募集日付 YYYY-MM-DD", time="開始時刻 HH:MM")
    async def createwolf(interaction, date: str, time: str):
        try:
            dt = datetime.fromisoformat(f"{date}T{time}")
            if dt.date() < (datetime.now() - timedelta(days=1)).date():
                await send_error(interaction.channel, interaction.user, "❌ 過去の日付に対する部屋は作成できません")
                return
        except ValueError:
            await send_error(interaction.channel, interaction.user, "❌ 日付・時刻のフォーマットが不正です")
            return

        # 部屋ID生成
        date_str = dt.strftime("%y%m%d")
        existing_files = list_events_by_date(date_str)
        seq = f"{int(max([f[6:8] for f in existing_files], default='0'))+1:02d}"
        event_id = f"{date_str}{seq}"

        events[event_id] = {
            "datetime": dt.isoformat(),
            # { "22:30": [{id, name, url, waitlist}, ...], ... }
            "participants": {},
            "channel_id": interaction.channel.id,
            "message_id": None,
            "list_message_id": None
        }
        save_event(event_id, events[event_id])

        # 募集メッセージ
        month_day = dt.strftime("%m月%d日")
        hour_min = dt.strftime("%H:%M")
        content = f"@everyone\n🚨アモアス募集🚨\n{month_day} {hour_min}~\n部屋ID:{event_id}"
        msg = await interaction.channel.send(content)
        events[event_id]["message_id"] = msg.id
        save_event(event_id, events[event_id])

        await interaction.response.send_message(f"募集作成完了（部屋ID: {event_id}）", ephemeral=True)
