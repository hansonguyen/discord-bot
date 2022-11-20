import discord
import secrets
from api import *

baseURL = 'https://pokeapi.co/api/v2/'
endpoint = 'pokemon'
x = 151

response = getData(baseURL, endpoint, x)
pokemon = getNames(response)

def getResponse(message: str) -> str:
    message = message.lower()

    if message == 'hello':
        return 'Hey there!'

    if message == '!random':
        return 'Random Pokemon: ' + getRandomPokemon(pokemon)

    if message == '!about':
        return 'PokeBot was developed by Hanson Nguyen using Python and the PokeAPI.\nTo learn more about the creator, visit https://hansonguyen.github.io/\nTo see source code, visit https://github.com/hansonguyen/discord-bot\nTo learn more about PokeAPI, visit https://pokeapi.co/'

    if message == '!help':
        return 'PokeBot v1.0\n`"hello"`: Greeting from Bot\n`"!random"`: Get random Pokemon from Generation 1\n`"!about"`: Learn about the bot'

    return 'I didn\'t understand what you said. Use "!help" for a list of commands.'

async def sendMessage(message, userMessage):
    try:
        response = getResponse(userMessage)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def runBot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is online!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        userMessage = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{userMessage}" in #{channel}')

        await sendMessage(message, userMessage)
    # Need token to run yourself
    client.run(secrets.TOKEN)