import discord
from discord.ext import commands

class About(commands.Cog):
    """about"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("About Cog Online")

    @commands.command(
        help='Prints information about the bot development',
        brief='Info about Pokébot',
    )
    async def about(self, ctx):
        await ctx.channel.send('PokéBot was developed by Hanson Nguyen using Python and the PokeAPI.\nTo learn more about the creator, visit https://hansonguyen.github.io/\nTo see source code, visit https://github.com/hansonguyen/discord-bot\nTo learn more about PokéAPI, visit https://pokeapi.co/')

async def setup(bot):
    await bot.add_cog(About(bot))