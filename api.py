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
            'name': item['name'].capitalize(),
            'url': item['url']
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

def getInfo(name, data):
    pokemonInfo = 'Not found'
    for item in data:
        if name.lower().capitalize() == item['name']:
            specificData = requests.get(item['url']).json()
            pokedexData = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{item["id"]}').json()
            pokemonInfo = {
                'weight': specificData['weight'] / 10,
                'height': specificData['height'] / 10,
                'types': [],
                'description': '', # NEED TO MAKE ENGLISH ALWAYS
                'hp': specificData['stats'][0]['base_stat'],
                'attack': specificData['stats'][1]['base_stat'],
                'defense': specificData['stats'][2]['base_stat'],
                'special_attack': specificData['stats'][3]['base_stat'],
                'special_defense': specificData['stats'][4]['base_stat'],
                'speed': specificData['stats'][5]['base_stat'],
                'sprite': specificData['sprites']['front_default']
            }
            if len(specificData['types']) > 1:
                for type in specificData['types']:
                    pokemonInfo['types'].append(type['type']['name'])
            else:
                pokemonInfo['types'].append(specificData['types'][0]['type']['name'])
            i = 0
            while pokedexData['flavor_text_entries'][i]['language']['name'] != 'en':
                i += 1
            pokemonInfo['description'] = pokedexData['flavor_text_entries'][i]['flavor_text']
    return pokemonInfo

def getRegionInfo(region):
    regionData = requests.get(f'https://pokeapi.co/api/v2/region/{region.lower()}').json()

    # Get generation and convert
    generation = regionData['main_generation']['name'].split('-')
    genNumRoman = generation[1]
    genNum = ''
    if genNumRoman == 'i':
        genNum = 1
    elif genNumRoman == 'ii':
        genNum = 2
    elif genNumRoman == 'iii':
        genNum = 3
    elif genNumRoman == 'iv':
        genNum = 4
    elif genNumRoman == 'v':
        genNum = 5
    elif genNumRoman == 'vi':
        genNum = 6
    elif genNumRoman == 'vii':
        genNum = 7
    elif genNumRoman == 'viii':
        genNum = 8
    
    info = {
        'gen': genNum,
        'locations': []
    }
    for location in regionData['locations']:
        info['locations'].append(' '.join(elem.capitalize() for elem in location['name'].split('-')))
    return info