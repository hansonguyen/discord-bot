import discord
from discord.ext import commands
from api import *

# Poke API
baseURL = 'https://pokeapi.co/api/v2/'
endpoint = 'pokemon'
response = getData(baseURL, endpoint)
pokemon = getNames(response)

class Pokemon(commands.Cog):
    """info, random, region, type"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pokémon Cog Online")

    @commands.command(
        help='Prints a random Pokémon. Can provide generation number from 1-9 or leave it blank to pick from all Pokémon',
        brief='Gives a random Pokémon',
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
            embed.title = 'Random Pokémon'
            embed.description = f'{randomMon}'
            embed.set_thumbnail(url=info['sprite'])
            await ctx.channel.send(embed=embed)
        elif gen > 0 and gen < 9:
            embed.title = f'Random Pokémon from {region} region'
            embed.description = f'{randomMon}'
            embed.set_thumbnail(url=info['sprite'])
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send('Not a valid argument for "!random" command. Try "!help random"')

    @commands.command(
        help='Prints basic information about a Pokémon, including stats, type(s), etc.',
        brief='Info about a Pokémon',
        usage='<pokémon>'
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

    @commands.command(
        help='Prints information about a specific type including strengths, weaknesses, and some Pokémon of that type',
        brief='Info about a type',
        usage='<type>'
    )
    async def type(self, ctx, name):
        info = getTypeInfo(name)
        embed = discord.Embed(
            title=f'{name.lower().capitalize()}',
            description=f'Class: {info["class"]}',
            color=0xFF5733
        )
        if len(info['strengths']) > 0:
            strengthsStr = ', '.join(info['strengths'])
        else:
            strengthsStr = 'None'
        if len(info['weaknesses']) > 0:
            weaknessesStr = ', '.join(info['weaknesses'])
        else:
            weaknessesStr = 'None'
        if len(info['no_effect']) > 0:
            no_effectStr = ', '.join(info['no_effect'])
        else:
            no_effectStr = 'None'
        embed.add_field(name='Strong Against', value=strengthsStr, inline=True)
        embed.add_field(name='Weak To', value=weaknessesStr, inline=True)
        embed.add_field(name='No Effect To', value=no_effectStr, inline=True)
        embed.add_field(name='Some Pokémon', value=', '.join(info['pokemon']), inline=False)
        embed.add_field(name='Some Moves', value=', '.join(info['moves']), inline=False)
        await ctx.channel.send(embed=embed)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        await ctx.channel.send('Sorry, I didn\'t recognize that command. Try using "!help" for a list of commands')

async def setup(bot):
    await bot.add_cog(Pokemon(bot))