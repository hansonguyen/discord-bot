import discord
import os
from discord.ext import commands
from pretty_help import PrettyHelp
import asyncio
import secrets

# Create new bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!', description='Simple bot based on PokeAPI', help_command=PrettyHelp(index_title='Categories'))

# Load Cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# On Ready
@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')

# Executes bot with token. Need to define before use
async def main():
    await load()
    await bot.start(secrets.TOKEN)

asyncio.run(main())