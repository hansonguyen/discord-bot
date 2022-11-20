import requests
import random

def getData(base, end, x):
    return requests.get(base + end + f'?limit={x}').json()

def getPages(data):
    return data['count']

def getNames(data):
    names = []
    count = 1
    for item in data['results']:
        pokemon = {
            'id': count,
            'name': item['name'].capitalize()
        }
        count += 1
        names.append(pokemon)
    return names

def getRandomPokemon(data):
    num = random.randint(1, 151)
    for item in data:
        if item['id'] == num:
            return item['name']