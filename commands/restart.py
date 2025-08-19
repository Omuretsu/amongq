import os
import sys


def register_restart_command(
        bot
):
    @bot.tree.command(
        name="restart",
        description="BOTを再起動します（管理者限定）"
    )
    async def restart(
        interaction
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ 管理者権限が必要です",
                ephemeral=True
            )
            return
        await interaction.response.send_message(
            "🔄 BOTを再起動します...",
            ephemeral=True
        )
        os.execv(
            sys.executable,
            [sys.executable] + sys.argv
        )
