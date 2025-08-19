import discord
from discord.ext import commands
from discord import app_commands  # ← これを追加


class CreateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@app_commands.command(name="create", description="新しい部屋を作成します")
@app_commands.describe(room_id="部屋ID（任意）", capacity="定員（未指定で13人）")
async def create(self, interaction: discord.Interaction, room_id: str, capacity: int = None):
    if room_id in self.bot.room_data:
        await interaction.response.send_message("その部屋IDはすでに存在します。", ephemeral=True)
        return

    # デフォルト値
    if capacity is None:
        capacity = 13

    # 制限チェック
    if not 4 <= capacity <= 15:
        await interaction.response.send_message("部屋の定員は 4～15 の範囲で設定してください。", ephemeral=True)
        return

    self.bot.room_data[room_id] = {
        "capacity": capacity,
        "participants": [],
        "waitlist": []
    }
    await interaction.response.send_message(f"部屋 {room_id} を作成しました。定員: {capacity}人", ephemeral=True)
