import discord
from discord.ext import commands
from api import *

# Poke API
baseURL = 'https://pokeapi.co/api/v2/'
endpoint = 'pokemon'
response = getData(baseURL, endpoint)
pokemon = getNames(response)

class Pokemon(commands.Cog):
    """random"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pokemon Cog Online")

    @commands.command(
        help='Prints a random Pokemon. Can provide generation number from 1-9 or leave it blank to pick from all Pokemon',
        brief='Prints a random Pokemon',
        usage='<gen>'
    )
    async def random(self, ctx, gen=0):
        if gen == 0:
            await ctx.channel.send('Random Pokemon: ' + getRandomPokemon(pokemon, gen))
        elif gen > 0 and gen < 10:
            await ctx.channel.send(f'Random Pokemon from Generation {gen}: ' + getRandomPokemon(pokemon, gen))
        else:
            await ctx.channel.send('Not a valid argument for "!random" command. Try "!help random"')

async def setup(bot):
    await bot.add_cog(Pokemon(bot))