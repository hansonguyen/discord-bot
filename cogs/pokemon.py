import discord
from discord.ext import commands
from api import *

# Poke API
baseURL = 'https://pokeapi.co/api/v2/'
endpoint = 'pokemon'
response = getData(baseURL, endpoint)
pokemon = getNames(response)

class Pokemon(commands.Cog):
    """info, random, region"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pokemon Cog Online")

    @commands.command(
        help='Prints a random Pokemon. Can provide generation number from 1-9 or leave it blank to pick from all Pokemon',
        brief='Gives a random Pokemon',
        usage='<gen #>'
    )
    async def random(self, ctx, gen=0):
        randomMon = getRandomPokemon(pokemon, gen)
        info = getInfo(randomMon, pokemon)
        region = ''
        if gen == 1:
            region = 'Kanto'
        elif gen == 2:
            region = 'Johto'
        elif gen == 3:
            region = 'Hoenn'
        elif gen == 4:
            region = 'Sinnoh'
        elif gen == 5:
            region = 'Unova'
        elif gen == 6:
            region = 'Kalos'
        elif gen == 7:
            region = 'Alola'
        elif gen == 8:
            region = 'Galar'
        embed = discord.Embed(
            color=0xFF5733
        )
        if gen == 0:
            embed.title = 'Random Pokemon'
            embed.description = f'{randomMon}'
            embed.set_thumbnail(url=info['sprite'])
            await ctx.channel.send(embed=embed)
        elif gen > 0 and gen < 9:
            embed.title = f'Random Pokemon from {region} region'
            embed.description = f'{randomMon}'
            embed.set_thumbnail(url=info['sprite'])
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send('Not a valid argument for "!random" command. Try "!help random"')

    @commands.command(
        help='Prints basic information about a Pokemon, including stats, type(s), etc.',
        brief='Info about a Pokemon',
        usage='<pokemon>'
    )
    async def info(self, ctx, name):
        info = getInfo(name, pokemon)
        embed = discord.Embed(
            title=f'{name.lower().capitalize()}',
            description=info['description'],
            color=0xFF5733
        )
        embed.set_thumbnail(url=info['sprite'])
        embed.add_field(name='Type(s)', value=info['types'], inline=False)
        embed.add_field(name='HP', value=info['hp'], inline=True)
        embed.add_field(name='Attack', value=info['attack'], inline=True)
        embed.add_field(name='Defense', value=info['defense'], inline=True)
        embed.add_field(name='Sp. Attack', value=info['special_attack'], inline=True)
        embed.add_field(name='Sp. Defense', value=info['special_defense'], inline=True)
        embed.add_field(name='Speed', value=info['speed'], inline=True)
        embed.add_field(name='Height', value=f'{info["height"]}m', inline=True)
        embed.add_field(name='Weight', value=f'{info["weight"]}kg', inline=True)
        await ctx.channel.send(embed=embed)

    @commands.command(
        help='Prints basic information about a region, including locations.',
        brief='Info about a region',
        usage='<region>'
    )

    async def region(self, ctx, name):
        regions = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos', 'alola', 'galar']
        info = getRegionInfo(name)
        embed = discord.Embed(
            title=f'{name.lower().capitalize()}',
            description=f'Main Generation: {info["gen"]}',
            color=0xFF5733
        )
        if len(info['locations']) > 0:
            sList = []
            for i in range(3):
                sList.append(info['locations'][i])
            smallList = ', '.join(sList)
        else:
            smallList = 'No locations found!'
        embed.add_field(name='Some locations', value=smallList, inline=False)
        await ctx.channel.send(embed=embed)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        await ctx.channel.send('Sorry, I didn\'t recognize that command. Try using "!help" for a list of commands')

async def setup(bot):
    await bot.add_cog(Pokemon(bot))