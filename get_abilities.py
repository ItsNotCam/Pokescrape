import requests, sqlite3
from dbops import init_db
from bs4 import BeautifulSoup
from tabulate import tabulate

from objects.ability import Ability

def add_abilities(pokemon, ability_names, conn):
	body = requests.get(f"http://pokemondb.net/ability")
	soup = BeautifulSoup(body.content, features="html.parser")

	if soup is not None:
		ability_rows = soup.select("#abilities tbody tr")
		for ability_row in ability_rows:
			ability_cols = ability_row.find_all("td")
			found_ability_name = ability_cols[0].find("a").get_text(strip=True).lower()
			for ability_name in ability_names:
				if ability_name.lower() == found_ability_name.lower():
					name, _, description, generation = [r.get_text(strip=True) for r in ability_cols]
					print(name, description, generation)

					conn.execute("INSERT OR IGNORE INTO abilities VALUES (?,?,?)", (name, description, generation))
					ability = Ability(ability_name, description, generation)
					ability_sql = "INSERT OR IGNORE INTO abilities VALUES (?,?,?)"

					print("adding ability to database:", ability.to_tuple())
					conn.execute(ability_sql, (ability.name, ability.description, ability.generation))

					pkmn_ability = (ability_name, pokemon.number, pokemon.name, pokemon.sub_name)
					print("adding pkmn_ability to database:", pkmn_ability)
					pkmn_ability_sql = "INSERT OR IGNORE INTO pokemon_abilities VALUES (?,?,?,?)"
					conn.execute(pkmn_ability_sql, pkmn_ability)

		conn.commit()