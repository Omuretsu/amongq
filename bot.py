import discord
from discord.ext import commands

from commands.create import CreateCommands
from commands.cancel import CancelCommands
from reactions.participant import ListCommands
from commands.set_capacity import SetCapacityCommands
from commands.set_default_capacity import SetDefaultCapacityCommands  # 管理者用コマンド

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# データ保存用（全commandsで共有）
bot.room_data = {}

# commandsのロード
bot.add_cog(CreateCommands(bot))
bot.add_cog(CancelCommands(bot))
bot.add_cog(ListCommands(bot))
bot.add_cog(SetCapacityCommands(bot))


@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

bot.run("ここにトークン")
