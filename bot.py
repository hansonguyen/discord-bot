import discord
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

    if message == '!help':
        return '`PokeBot\n"hello": Greeting from Bot\n"!random": Get random Pokemon from Generation 1`'

    return 'I didn\'t understand what you said. Use "!help" for a list of commands.'

async def sendMessage(message, userMessage):
    try:
        response = getResponse(userMessage)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def runBot():
    TOKEN = 'MTA0MzczOTc1NzI4MjMzNjgyMA.G5dzn3.gIyYvizNAwyIpjXaLb-A97hJNSkS7sJVDeEd0I'
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
    client.run(TOKEN)