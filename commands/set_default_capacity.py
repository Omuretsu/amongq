import discord
from discord.ext import commands
from discord import app_commands
from commands import save_default_capacity


class SetDefaultCapacityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setdefaultcapacity",
        description="今後作成される部屋の定員を変更します（サーバー管理者専用）"
    )
    @app_commands.describe(new_capacity="新しい定員")
    async def set_default_capacity(self, interaction: discord.Interaction, new_capacity: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("サーバーの管理者権限が必要です。", ephemeral=True)
            return
        if new_capacity < 1:
            await interaction.response.send_message("定員は1以上で指定してください。", ephemeral=True)
            return

        # 永続化
        save_default_capacity(new_capacity)
        await interaction.response.send_message(f"今後作成される部屋の定員を {new_capacity} 人に変更しました。", ephemeral=True)


async def setup(bot):
    await bot.add_cog(SetDefaultCapacityCommands(bot))
