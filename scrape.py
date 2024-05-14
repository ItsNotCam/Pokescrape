import requests, sys,asyncio, re
from bs4 import BeautifulSoup
import aiofiles as aiof
from tabulate import tabulate

from lib.data_types import *
from lib import pokestats, db

from lib.models import Pokemon

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
		abilities_selection = soup2.select("th:-soup-contains('Abilities') + td span a")
		if abilities_selection is not None and len(abilities_selection) > 0:
			ABILITIES.append(abilities_selection[0].get_text(strip=True))
		
		return (SPECIES, HEIGHT, WEIGHT, ABILITIES)

def get_training_data(soup2):
		training_selection = soup2.select("h2:-soup-contains('Training') + table tr")

		CATCH_RATE_NUMBER = CATCH_RATE_PERCENT = 0
		if len(training_selection) > 1:
			CATCH_RATE_NUMBER, CATCH_RATE_PERCENT = pokestats.get_catch_rate(training_selection[1])

		FRIENDSHIP_NUMBER = FRIENDSHIP_EXTREMITY = 0
		if len(training_selection) > 2:
			FRIENDSHIP_NUMBER, FRIENDSHIP_EXTREMITY = pokestats.get_friendship(training_selection[2])
		
		BASE_EXP = 0
		if len(training_selection) > 3:
			BASE_EXP = pokestats.get_exp(training_selection[3])

		GROWTH_RATE = ""
		if len(training_selection) > 4:
			GROWTH_RATE = pokestats.get_growth_rate(training_selection[4])

		return TrainingData(CATCH_RATE_NUMBER, CATCH_RATE_PERCENT, FRIENDSHIP_NUMBER, FRIENDSHIP_EXTREMITY, BASE_EXP, GROWTH_RATE)

def get_breeding_data(soup):
	breeding_data = soup.select("h2:-soup-contains('Breeding') + table tbody tr")
	if breeding_data is None or len(breeding_data) < 3:
		print("Weird reeding data found | len:", len(breeding_data))
		print("\n".join(["'" + b.get_text(strip=True) + "'" for b in breeding_data]))
		print("\n")
		return (None, None, None, None, None, None)

	EGG_GROUPS = pokestats.get_egg_groups(breeding_data[0])
	GENDER_MALE, GENDER_FEMALE = pokestats.get_gender_data(breeding_data[1])
	EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, EGG_CYCLES_STEPS_MAX = pokestats.get_egg_cycles(breeding_data[2])

	return BreedingData(EGG_GROUPS, GENDER_MALE, GENDER_FEMALE, EGG_CYCLES_NUMBER, EGG_CYCLES_STEPS_MIN, EGG_CYCLES_STEPS_MAX)

def get_physical_data(soup):
	POKEMON_SPECIES = pokestats.get_pokemon_species(soup)
	POKEMON_HEIGHT = pokestats.get_pokemon_height(soup)
	POKEMON_WEIGHT = pokestats.get_pokemon_weight(soup)
	return PhysicalData(POKEMON_SPECIES, POKEMON_HEIGHT, POKEMON_WEIGHT)

def soup_to_int(soup):
	return int(soup.get_text(strip=True))

def get_img_name(name, sub_name):
	img_name = f"{name}"
	if sub_name is not None and len(sub_name) > 0:
		sub_name_cleaned = sub_name.replace(" ", "_").strip()
		img_name = f"{name}_{sub_name_cleaned}"
	return f"{img_name.lower()}.png"

def scrape(download_icons=False, download_images=False, start_number=None, end_number=None, debug=False, cnx=None):
	soup = BeautifulSoup(
		requests.get("https://pokemondb.net/pokedex/all").content, 
		features="html.parser"
	)
 
	pokedex_table = soup.body.find(id="pokedex").find("tbody").find_all("tr")

	for pokedex_row_soup in pokedex_table:
		num_soup, name_soup, elements_soup, total_soup, hp_soup, attack_soup, \
		defense_soup, sp_att_soup, sp_def_soup, speed_soup = pokedex_row_soup.find_all("td")

		POKEMON_NUMBER = int(get_tag(num_soup, "span"))
		if start_number and POKEMON_NUMBER < start_number:
			continue
		if end_number and POKEMON_NUMBER > end_number:
			return

		POKEMON_NAME, POKEMON_SUB_NAME = pokestats.get_pokemon_name(pokedex_row_soup, name_soup)
		POKEMON_LINK = pokestats.get_pokemon_link(name_soup)

		# Getting more detailed pokemon data
		pokemon_soup = BeautifulSoup(
			requests.get(f"https://pokemondb.net{POKEMON_LINK}").content, 
			features="html.parser"
		)
		
		stats_data = PokemonStatsData(
			soup_to_int(total_soup), 
			soup_to_int(hp_soup),
			soup_to_int(attack_soup),
			soup_to_int(defense_soup),
			soup_to_int(sp_att_soup),
			soup_to_int(sp_def_soup),
			soup_to_int(speed_soup),
		)
		physical_data = get_physical_data(pokemon_soup)
		training_data = get_training_data(pokemon_soup)
		breeding_data = get_breeding_data(pokemon_soup)

		img_name = get_img_name(POKEMON_NAME, POKEMON_SUB_NAME)
		new_pokemon = Pokemon(
			POKEMON_NUMBER, 
			POKEMON_NAME, 
			POKEMON_SUB_NAME, 
			img_name,
			stats_data,
			physical_data,
			training_data,
			breeding_data
		)

		abilities = pokestats.get_pokemon_abilies(pokemon_soup)
		elements = pokestats.get_pokemon_elements(elements_soup)
		moves = pokestats.get_pokemon_moves(pokemon_soup)
		evs = pokestats.get_pokemon_evs(new_pokemon, pokemon_soup)
		
		print("--------------------------------------")
		print(f"Adding #{new_pokemon.number} {new_pokemon.name} to database")
		if debug:
			abilities_str = ", ".join(abilities)
			elements_str = ", ".join(elements)
			moves_str = tabulate(
				[m.to_tuple() for m in moves], 
				headers= ["Source", "Name", "Level"], 
				tablefmt="outline"
			)
			ev_str = tabulate(
				[ev.to_tuple() for ev in evs], 
				headers=["Name", "pkmn #", "pkmn name", "pkmn subname", "Amount"], 
				tablefmt="outline"
			)

			print("")
			print(f"ABILITIES: {abilities_str}\n")
			print(f"ELEMENTS: {elements_str}\n")
			print(f"EVS:\n{ev_str}\n\n")
			print(f"MOVES:\n{moves_str}\n")

		print("--------------------------------------\n")

		db.add_pokemon_to_database(new_pokemon, abilities, elements, moves, evs, cnx)

		if download_images:
			loop.run_until_complete(download_pkmn_img(POKEMON_NAME, f"images/{img_name}.png", f"https://pokemondb.net{POKEMON_LINK}"))
		if download_icons:
			loop.run_until_complete(download_image(num_soup.find("picture").find("img")["src"], f"icons/{img_name}.png"))
		
	cnx.commit()
 
if __name__ == "__main__":
	scrape(False, sys.argv[1])