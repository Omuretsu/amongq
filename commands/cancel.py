from utils.persistence import save_event


def register_cancel_command(bot, events):
    @bot.tree.command(name="cancelamong", description="募集を流会にする")
    async def cancelroom(interaction, event_id: str):
        if event_id not in events:
            await interaction.response.send_message("❌ 部屋IDが見つかりませんでした", ephemeral=True)
            return

        event = events[event_id]
        channel = interaction.guild.get_channel(event["channel_id"])

        # 募集メッセージ・一覧メッセージ削除
        try:
            msg = await channel.fetch_message(event["message_id"])
            await msg.delete()
        except:
            pass
        try:
            msg = await channel.fetch_message(event.get("list_message_id"))
            await msg.delete()
        except:
            pass

        dt = event.get("datetime")
        from datetime import datetime
        dt_obj = datetime.fromisoformat(dt)
        month_day = dt_obj.strftime("%m月%d日")
        hour_min = dt_obj.strftime("%H:%M")

        await channel.send(f"{month_day} {hour_min}からのゲーム（開催ID：{event_id}）は流会となりました")
