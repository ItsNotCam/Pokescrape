from bs4 import BeautifulSoup
import requests, re

from lib import db as DB
from lib.models import Move, Ability

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

from lib.models import PokemonMove, PokemonEV
import re

def get_tag_all(element, selector):
  return [e.text.strip() for e in element.find_all(selector)]

def get_tag(element, selector):
  return element.find(selector).text.strip()

def get_pokemon_abilies(soup):
	ability_names = []

	abilities_selection = soup.select("th:-soup-contains('Abilities') + td span a")
	if abilities_selection is not None and len(abilities_selection) > 0:
		ability_names.append(abilities_selection[0].get_text(strip=True))

	return ability_names

def get_pokemon_elements(soup):
	return [e for e in get_tag_all(soup, "a")]

def get_pokemon_moves(soup):
	level_up_moves_soup = []
	egg_moves_soup = []
	tm_moves_soup = []

	h3s = soup.find_all("h3")
	for h3 in h3s:
		txt = h3.get_text(strip=True)
		if txt == "Moves learnt by level up":
			s = h3.find_next_sibling("div") #, class_="resp-scroll"
			if s:
				level_up_moves_soup = s.select("tbody tr")
		if txt == "Egg moves":
			s = h3.find_next_sibling("div") #, class_="resp-scroll"
			if s:
				egg_moves_soup = s.select("tbody tr")
		if txt == "Moves learnt by TM":
			s = h3.find_next_sibling("div") #, class_="resp-scroll"
			if s:
				tm_moves_soup = s.select("tbody tr")

	all_moves = []
	for move in level_up_moves_soup:
		name = move.find("a").get_text(strip=True)
		level = move.find_all("td")[0].get_text()
		try:
			level = int(level)
			all_moves.append(
				PokemonMove("Level Up", name, level)
			)
		except:
			print("failed to parse level number from move", level)
			level = -999

	for move in egg_moves_soup:
		name = move.find("a").get_text(strip=True)
		all_moves.append(
			PokemonMove("Egg", name, None)
		)

	for move in tm_moves_soup:
		name = None
		name_soup = move.find_all("a")
		if name_soup:
			name = name_soup[1].get_text(strip=True)
		all_moves.append(
			PokemonMove("TM", name, None)
		)

	return all_moves

def get_pokemon_evs(pokemon, soup):
	evs = []
	ev_selection = soup.select("th:-soup-contains('EV yield') + td")
	if len(ev_selection) > 0:
		ev_list = ev_selection[0].get_text(strip=True).split(", ")
		for ev in ev_list:
			ev_split = ev.split(" ")
			amount = int(ev_split[0])
			name = " ".join(ev_split[1::])
			evs.append(PokemonEV(
				name, 
				pokemon.number,
				pokemon.name, 
				pokemon.sub_name, 
				amount
			))

	return evs

def get_pokemon_species(soup):
	species = None
	species_selection = soup.select("th:-soup-contains('Species') + td")
	if len(species_selection) > 0:
		species = species_selection[0].get_text()
	return species

def get_pokemon_height(soup):
	height = 0
	height_selection = soup.select("th:-soup-contains('Height') + td")
	if len(height_selection) > 0:
		height = float(height_selection[0].get_text().split(" ")[0].replace("m","").strip())
	return height

def get_pokemon_weight(soup):
	weight = 0
	weight_selection = soup.select("th:-soup-contains('Weight') + td")
	if len(weight_selection) > 0:
		weight = float(weight_selection[0].get_text().split(" ")[0].replace("kg","").strip())
	return weight

def get_pokemon_name(pokemon_soup, name_soup):
	name_small_element = pokemon_soup.find("small")
	sub_name = ''
	if name_small_element is not None and len(name_small_element) > 0:
		sub_name = name_small_element.text.strip()
	name = get_tag(name_soup, "a")
	return (name, sub_name)

def get_pokemon_link(soup):
	return soup.find("a")["href"]

def get_catch_rate(soup):
	inner_text = soup.select("td")[0].get_text(strip=True)
	match = re.match(r"(\d{0,})\((\d{0,}.\d)%", inner_text)
	if match is not None:
		groups = match.groups()
		return (int(groups[0]), float(groups[1]))
	return (None,None)

def get_friendship(soup):
	inner_text = soup.select("td")[0].get_text(strip=True)
	match = re.match(r"(\d{0,}).\((\w{0,})\)", inner_text)
	if match is not None:
		groups = match.groups()
		return (int(groups[0]), groups[1].strip())
	return (None, None)

def get_exp(soup):
	inner_text = soup.select("td")[0].get_text(strip=True)
	try:
		return int(inner_text)
	except:
		return None
	
def get_growth_rate(soup):
	return soup.select("td")[0].get_text(strip=True)

def get_egg_groups(soup):
	return soup.find("a").get_text(strip=True)

def get_egg_cycles(soup):
	def to_int(str):
		return int(str.replace(",",""))

	cycles = re.findall(r"\d[\d,]+", soup.find("td").get_text())

	EGG_CYCLES_NUMBER = None
	EGG_CYCLES_STEPS_MIN = None
	EGG_CYCLES_STEPS_MAX = None
	
	if cycles is None:
		print("Failed to get egg cycles using regex")
	elif len(cycles) == 3:
		EGG_CYCLES_NUMBER = to_int(cycles[0])
		EGG_CYCLES_STEPS_MIN = to_int(cycles[1])
		EGG_CYCLES_STEPS_MAX = to_int(cycles[2])
	else:
		print("The number of cycles for some reason isnt 3... its", len(cycles))

	return (EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, EGG_CYCLES_STEPS_MAX)

def get_gender_data(soup):
	def convert_to(val, type):
		try:
			return type(val)
		except:
			return None

	gender_text = soup.find("td").get_text(strip=True)

	gender_matches = re.findall(r"(?:(\d+)|(\d+\.\d+))% (male|female)", gender_text)
	GENDER_MALE = None
	GENDER_FEMALE = None

	for matches in gender_matches:
		int_val, float_val, gender = matches

		if gender == 'male':
			if len(int_val) > 0:
				GENDER_MALE = convert_to(int_val, int)
			elif len(float_val) > 0:
				GENDER_MALE = convert_to(float_val, float)

		elif gender == 'female':
			if len(int_val) > 0:
				GENDER_FEMALE = convert_to(int_val, int)
			elif len(float_val) > 0:
				GENDER_FEMALE = convert_to(float_val, float)
	
	return (GENDER_MALE, GENDER_FEMALE)
