from bs4 import BeautifulSoup
import requests, re

from lib import db as DB
from models import Move, Ability

def get_tag(element, selector):
  return element.find(selector).get_text(strip=True)

def to_number(str):
	if str.isdigit():
		return int(str)
	return None	

def get_all_moves(conn):
	print("\nGetting all moves...")

	URL = "https://pokemondb.net/move/all"
	body = requests.get(URL).content
	soup = BeautifulSoup(body, features="html.parser")
	moves_soup = soup.body.find(id="moves").find("tbody").find_all("tr")

	for idx, move_soup in enumerate(moves_soup):
		name_soup, element_soup, dmg_category_soup, power_soup, \
		accuracy_soup, pp_soup, description_soup, probability_soup = move_soup.find_all("td")

		dmg_category = "-"
		img_soup = dmg_category_soup.find("img")
		if img_soup is not None:
			dmg_category = img_soup["alt"]	
		else:
			dmg_category = "-"

		new_move = Move(
			get_tag(name_soup, "a"), 
			get_tag(element_soup, "a"), 
			dmg_category, 		
			to_number(power_soup.text.strip()),
			to_number(accuracy_soup.text.strip()),
			to_number(pp_soup.text.strip()),
			description_soup.text.strip(),
			to_number(probability_soup.text.strip())
		)

		print(f"{idx+1}) {new_move.to_tuple()}")
		DB.add_move_to_database(new_move, conn)

	conn.commit() 

def get_all_abilities(conn):
	print("\nGetting all abilities...")

	URL = "https://pokemondb.net/ability"
	body = requests.get(URL).content
	soup = BeautifulSoup(body, features="html.parser")
	abilities = soup.body.find(id="abilities").find("tbody").find_all("tr")

	for idx, ability in enumerate(abilities):
		name_soup, _, description_soup, generation_soup = ability.find_all("td")

		name = get_tag(name_soup, "a")
		description = description_soup.get_text(strip=True)
		generation = int(generation_soup.get_text(strip=True))
		new_ability = Ability(name, description, generation) 

		print(f"{idx+1}) {new_ability.name}: {new_ability.description}")
		DB.add_ability_to_database(new_ability, conn)
		
	conn.commit() 

def get_dmg_effectiveness(conn):
	print("\nGetting damage effectiveness")
	
	URL = "https://pokemondb.net/type"
	body = requests.get(URL).content
	soup = BeautifulSoup(body, features="html.parser")

	type_effectiveness_soup = soup.select(".type-fx-cell")
	for eff_soup in type_effectiveness_soup:
		effect = eff_soup.get("title")
		dmg_src, dmg_dst, effect = re.match(r"(?:(.*) → (.*)) = (.*)", effect).groups()

		effect_number = -1
		if effect == 'no effect':
			effect_number = 0
		elif effect == 'not very effective':
			effect_number = 0.5
		elif effect == 'normal effectiveness':
			effect_number = 1
		elif effect == 'super-effective':
			effect_number = 2

		print(f"\'{effect}\'", effect_number)
		
		DB.add_dmg_effectiveness(dmg_src, dmg_dst, effect_number, conn)
		
	conn.commit() 

if __name__ == '__main__':
	get_dmg_effectiveness()