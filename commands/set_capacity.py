# commands/setcapacity.py
import discord
from discord.ext import commands
from discord import app_commands


class SetCapacityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setcapacity",
        description="作成された部屋の定員を増やします（誰でも実行可能）"
    )
    @app_commands.describe(
        room_id="定員を変更する部屋ID",
        new_capacity="新しい定員（14か15のみ）"
    )
    async def setcapacity(self, interaction: discord.Interaction, room_id: str, new_capacity: int):
        if room_id not in self.bot.room_data:
            await interaction.response.send_message("その部屋は存在しません。", ephemeral=True)
            return

        current_capacity = self.bot.room_data[room_id]["capacity"]

        if new_capacity <= current_capacity:
            await interaction.response.send_message(
                f"定員は現在より増やす必要があります（現在: {current_capacity}人）",
                ephemeral=True
            )
            return

        if new_capacity not in [14, 15]:
            await interaction.response.send_message(
                "作成後に設定できる定員は14か15のみです。",
                ephemeral=True
            )
            return

        self.bot.room_data[room_id]["capacity"] = new_capacity
        await interaction.response.send_message(
            f"部屋 {room_id} の定員を {new_capacity} 人に変更しました。",
            ephemeral=True
        )
