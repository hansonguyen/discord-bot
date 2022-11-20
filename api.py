import requests
import random

def getData(base, end):
    return requests.get(base + end + f'?limit=905').json()

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

def getRandomPokemon(data, gen=0):
    if gen == 1:
        num = random.randint(1, 151)
    elif gen == 2:
        num = random.randint(152, 251)
    elif gen == 3:
        num = random.randint(252, 386)
    elif gen == 4:
        num = random.randint(387, 493)
    elif gen == 5:
        num = random.randint(494, 649)
    elif gen == 6:
        num = random.randint(650, 721)
    elif gen == 7:
        num = random.randint(722, 809)
    elif gen == 8:
        num = random.randint(810, 905)
    else:
        num = random.randint(1, 905)

    for item in data:
        if item['id'] == num:
            return item['name']