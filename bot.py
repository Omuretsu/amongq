# ── .env からトークンを読み込む ──
from utils.persistence import load_all_events
from reactions.participant import handle_reaction_add, handle_reaction_remove
from commands.restart import register_restart_command
from commands.cancel import register_cancel_command
from commands.create import register_create_command
from config import BOT_TOKEN
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os

load_dotenv()  # 同階層の .env を読み込む
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
events = load_all_events()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

register_create_command(bot, events)
register_cancel_command(bot, events)
register_restart_command(bot)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    await handle_reaction_add(reaction, user, events, bot)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    await handle_reaction_remove(reaction, user, events, bot)

# .env から読み込んだトークンで起動
bot.run(TOKEN)
