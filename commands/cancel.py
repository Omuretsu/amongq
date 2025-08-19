import discord
from discord.ext import commands
from discord import app_commands


class Cancelcommands(
    commands.Cog
):
    def __init__(
            self,
            bot
    ):
        self.bot = bot

    @app_commands.command(
        name="cancel",
        description="部屋からキャンセルします"
    )
    @app_commands.describe(
        room_id="キャンセルする部屋ID"
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        room_id: str
    ):
        if room_id not in self.bot.room_data:
            await interaction.response.send_message(
                "その部屋は存在しません。",
                ephemeral=True
            )
            return

        # 参加者リストから削除
        participant = next(
            (p for p in self.bot.room_data[room_id]["participants"] if p["name"] == interaction.user.name), None)
        if participant:
            self.bot.room_data[room_id]["participants"].remove(participant)
            # 補欠がいれば繰り上げ
            if self.bot.room_data[room_id]["waitlist"]:
                promoted = self.bot.room_data[room_id]["waitlist"].pop(0)
                new_code = len(self.bot.room_data[room_id]["participants"]) + 1
                self.bot.room_data[room_id]["participants"].append(
                    {"name": promoted["name"], "code": new_code})
            await interaction.response.send_message("参加をキャンセルしました。", ephemeral=True)
            return

        # 補欠リストから削除
        wait = next(
            (w for w in self.bot.room_data[room_id]["waitlist"] if w["name"] == interaction.user.name), None)
        if wait:
            self.bot.room_data[room_id]["waitlist"].remove(wait)
            await interaction.response.send_message("補欠参加をキャンセルしました。", ephemeral=True)
            return

        await interaction.response.send_message("あなたはこの部屋に参加していません。", ephemeral=True)
