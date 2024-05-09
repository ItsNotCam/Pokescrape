from lib.pokestats import get_pokemon_moves
from bs4 import BeautifulSoup
import requests

content = requests.get("https://pokemondb.net/pokedex/charmander").content
soup = BeautifulSoup(content, features='html.parser')

moves = get_pokemon_moves(soup)
for move in moves:
	print(move.level, move.move_name, "\t", move.source)