from dbops import init_db, add_pokemon_to_database
import requests, sys, json, sqlite3, asyncio, os, re
from objects.pokemon import Pokemon
from tabulate import tabulate
from bs4 import BeautifulSoup
import aiofiles as aiof

import sqlite3


loop = asyncio.get_event_loop()

def get_tag(element, selector):
  return element.find(selector).text.strip()

def get_tag_all(element, selector):
  return [e.text.strip() for e in element.find_all(selector)]

async def download_image(img_url, img_path):
  with requests.get(img_url) as img_data:
    if img_data is not None:
      async with aiof.open(img_path, 'wb') as img:
        await img.write(img_data.content)
        await img.flush()

async def download_pkmn_img(name, file_path, link):
	body = requests.get(link).content
	soup = BeautifulSoup(body, features="html.parser")
  
	element = soup.find(attrs={"data-title": re.compile(r".*official artwork$")})
	if element is not None:
		img_url = element["href"]
		await download_image(img_url, file_path)
	else:
		element = [a for a in soup.find_all("img") if name.lower() in a["alt"].lower()][0]
		img_url = element.get("src")
		await download_image(img_url, file_path)

def get_pokedex_data(soup2):
		SPECIES = ""
		species_selection = soup2.select("th:-soup-contains('Species') + td")
		if len(species_selection) > 0:
			SPECIES = species_selection[0].get_text()

		HEIGHT = 0
		height_selection = soup2.select("th:-soup-contains('Height') + td")
		if len(height_selection) > 0:
			HEIGHT = float(height_selection[0].get_text().split(" ")[0].replace("m","").strip())

		WEIGHT = 0
		weight_selection = soup2.select("th:-soup-contains('Weight') + td")
		if len(weight_selection) > 0:
			WEIGHT = float(weight_selection[0].get_text().split(" ")[0].replace("kg","").strip())

		ABILITIES = []
		abilities_selection = soup2.select("th:-soup-contains('Abilities') + td")
		if len(abilities_selection) > 0:
			for ability in abilities_selection[0].select(".text-muted"):
				ABILITIES.append(ability.find("a").get_text(strip=True))
		
		return (SPECIES, HEIGHT, WEIGHT, ABILITIES)

def get_training_data(soup2):
		training_selection = soup2.select("h2:-soup-contains('Training') + table tr")

		EV_NUMBERS = []
		EV_TYPES = []
		ev_selection = soup2.select("th:-soup-contains('EV yield') + td")
		if len(ev_selection) > 0:
			ev_list = ev_selection[0].get_text(strip=True).split(", ")
			for ev in ev_list:
				ev_split = ev.split(" ")
				EV_NUMBERS.append(int(ev_split[0]))
				EV_TYPES.append(" ".join(ev_split[1::]))

		CATCH_RATE_NUMBER = 0
		CATCH_RATE_PERCENT = 0
		if len(training_selection) > 1:
			inner_text = training_selection[1].select("td")[0].get_text(strip=True)
			match = re.match(r"(\d{0,})\((\d{0,}.\d)%", inner_text)
			if match is not None:
				groups = match.groups()
				CATCH_RATE_NUMBER = int(groups[0])
				CATCH_RATE_PERCENT = float(groups[1])

		FRIENDSHIP_NUMBER = 0
		FRIENDSHIP_EXTREMITY = 0
		if len(training_selection) > 2:
			inner_text = training_selection[2].select("td")[0].get_text(strip=True)
			match = re.match(r"(\d{0,}).\((\w{0,})\)", inner_text)
			if match is not None:
				groups = match.groups()
				FRIENDSHIP_NUMBER = int(groups[0])
				FRIENDSHIP_EXTREMITY = groups[1].strip()
			else:
				print("No Match for friendship section")
		
		BASE_EXP = 0
		if len(training_selection) > 3:
			inner_text = training_selection[3].select("td")[0].get_text(strip=True)
			BASE_EXP = int(inner_text)

		GROWTH_RATE = ""
		if len(training_selection) > 4:
			GROWTH_RATE = training_selection[4].select("td")[0].get_text(strip=True)

		return (EV_NUMBERS, EV_TYPES, CATCH_RATE_NUMBER, CATCH_RATE_PERCENT, FRIENDSHIP_NUMBER, \
		FRIENDSHIP_EXTREMITY, BASE_EXP, GROWTH_RATE)

def get_breeding_data(soup2):
	breeding_data = soup2.select("h2:-soup-contains('Breeding') + table tbody tr")
	if breeding_data is None or len(breeding_data) < 3:
		print("Weird reeding data found | len:", len(breeding_data))
		print("\n".join(["'" + b.get_text(strip=True) + "'" for b in breeding_data]))
		print("\n")
		return ("", -1, -1, -1, -1, -1)

	egg_groups, gender, egg_cycles = breeding_data[0:3]

	EGG_GROUPS = egg_groups.find("a").get_text(strip=True)
	
	GENDER_MALE = 0
	GENDER_FEMALE = 0
	genders = re.findall(r"(?:(\d+)|(\d+\.\d+))% (male|female)", gender.find("td").get_text(strip=True))
	for gender in genders:
		percentage, name = [g for g in gender if len(g) > 0]
		if name == 'female':
			GENDER_FEMALE = float(percentage)
		else:
			GENDER_MALE = float(percentage)

	egg_cycles = re.findall(r"\d[\d,]+", egg_cycles.find("td").get_text())

	EGG_CYCLES_NUMBER = int(egg_cycles[0])
	EGG_CYCLES_STEPS_MIN = int(egg_cycles[1].replace(",", ""))
	EGG_CYCLES_STEPS_MAX = int(egg_cycles[2].replace(",", ""))

	return (EGG_GROUPS, GENDER_MALE, GENDER_FEMALE, EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, \
		EGG_CYCLES_STEPS_MAX)

def scrape(download_images, start_index):
	body = requests.get("https://pokemondb.net/pokedex/all").content
	soup = BeautifulSoup(body, features="html.parser")

	# with open('pages/pokemon.html', 'w') as file:
	# 	file.write(BeautifulSoup.prettify(soup))
	# html = ""
	# with open('pages/pokemon.html', 'r') as file:
	# 	html = file.read()
	# soup = BeautifulSoup(html, features="html.parser")
 
	pokedex_table = soup.body.find(id="pokedex").find("tbody").find_all("tr")
	pokedex_table = pokedex_table[start_index:start_index+20]

	for idx, pokemon in enumerate(pokedex_table):
		num, name, elements, total, hp, attack, defense, sp_att, sp_def, speed = pokemon.find_all("td")
		
		# Get small subtitle name
		name_small_element = pokemon.find("small")
		sub_name = ""
		if name_small_element is not None and len(name_small_element) > 0:
			sub_name = name_small_element.text.strip()

		elements = [e.lower() for e in get_tag_all(elements, "a")]
		POKEMON_NAME, pokemon_link = (get_tag(name, "a").lower(), name.find("a")["href"])
		
		img_name = f"{POKEMON_NAME}".lower()
		if sub_name is not None and len(sub_name) > 0:
			sub_name_cleaned = sub_name.replace(" ", "_").strip()
			img_name = f"{POKEMON_NAME}_{sub_name_cleaned}".lower()
		
		if download_images:
			loop.run_until_complete(download_pkmn_img(POKEMON_NAME, f"images/{img_name}.png", f"https://pokemondb.net{pokemon_link}"))
			loop.run_until_complete(download_image(num.find("picture").find("img")["src"], f"icons/{img_name}.png"))

		POKEMON_NAME, pokemon_link = (get_tag(name, "a").lower(), name.find("a")["href"])

		# Getting more detailed pokemon data
		body2 = requests.get(f"https://pokemondb.net{pokemon_link}").content
		soup2 = BeautifulSoup(body2, features="html.parser")
		
		SPECIES, HEIGHT, WEIGHT, ABILITIES = get_pokedex_data(soup2)
		
		EV_NUMBERS, EV_TYPES, CATCH_RATE_NUMBER, CATCH_RATE_PERCENT, FRIENDSHIP_NUMBER, \
		FRIENDSHIP_EXTREMITY, BASE_EXP, GROWTH_RATE = get_training_data(soup2)

		EGG_GROUPS, GENDER_MALE_PERCENT, GENDER_FEMALE_PERCENT, EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, \
		EGG_CYCLES_STEPS_MAX = get_breeding_data(soup2)


		# print(idx, POKEMON_NAME, SPECIES, HEIGHT, WEIGHT, EV_NUMBERS, EV_TYPES, ABILITIES, \
		# 		f"{CATCH_RATE_NUMBER} {CATCH_RATE_PERCENT}%", FRIENDSHIP_NUMBER, FRIENDSHIP_EXTREMITY, BASE_EXP, \
		# 			GROWTH_RATE, EGG_GROUPS, GENDER_MALE_PERCENT, GENDER_FEMALE_PERCENT, EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, \
		# 			EGG_CYCLES_STEPS_MAX)

		SPECIES = ""
		species_selection = soup2.select("th:-soup-contains('Species') + td")
		if len(species_selection) > 0:
			SPECIES = species_selection[0].get_text()
			# new_pokemon = new_pokemon + (species, )
		
		HEIGHT = 0
		height_selection = soup2.select("th:-soup-contains('Height') + td")
		if len(height_selection) > 0:
			height_text = height_selection[0].get_text()
			height_text = height_text.split(" ")[0]
			HEIGHT = float(height_text.replace("m", "").strip())
		else:
			print("Failed to get height")

		n = EV_NUMBERS[0]
		t = EV_TYPES[0]

		new_pokemon = Pokemon(
			int(get_tag(num, "span")), 
			POKEMON_NAME, sub_name, f"{img_name}.png",
			int(total.text.strip()),
			int(hp.text.strip()),
			int(attack.text.strip()),
			int(defense.text.strip()),
			int(sp_att.text.strip()),
			int(sp_def.text.strip()),
			int(speed.text.strip()),
			SPECIES, HEIGHT, WEIGHT, n, t, CATCH_RATE_NUMBER,
			CATCH_RATE_PERCENT, FRIENDSHIP_NUMBER, FRIENDSHIP_EXTREMITY,
			BASE_EXP, GROWTH_RATE, GENDER_MALE_PERCENT, GENDER_FEMALE_PERCENT,
			EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, EGG_CYCLES_STEPS_MAX,
		)

		# new_pokemon.print()
		# print("\n")

		print(f"{idx+1+start_index} - Adding {new_pokemon.to_tuple()} - {elements} to database")
		add_pokemon_to_database(new_pokemon, elements, ABILITIES, sqlite3.connect('db/pokemon.db'))

	# else:
	# 	element_type = sys.argv[1].strip()
	# 	cursor = conn.cursor()
	# 	rows = cursor.execute("""
	# 		SELECT p.number, p.name || " " || p.sub_name as 'full name', GROUP_CONCAT(pt.element_name, ","), 
	# 			p.attack, p.defense, p.special_attack, p.special_defense, p.speed, p.hp
	# 		FROM pokemon as p
	# 		JOIN pokemon_type as pt ON pt.pokemon_number = p.number AND pt.pokemon_name = p.name AND pt.pokemon_sub_name = p.sub_name
	# 		GROUP BY p.number, p.name, p.sub_name
	# 		ORDER BY MAX(p.hp) ASC LIMIT 50
	# 	""").fetchall()

	# 	print(f"All {len(rows)} {element_type} types")
	# 	print(tabulate(rows, headers=['#', 'Name', 'Elements', 'Att', 'Def', 'Sp.Att.', 'Sp.Def.', 'Speed', 'HP'], tablefmt='pretty', stralign='left'))

	# 	cursor.close()