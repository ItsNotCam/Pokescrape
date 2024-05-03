from dbops import init_db, add_pokemon_to_database
import requests, sys, json, sqlite3, asyncio, os
from objects.pokemon import Pokemon
from tabulate import tabulate
from bs4 import BeautifulSoup
import aiofiles as aiof

loop = asyncio.get_event_loop()

def get_tag(element, selector):
  return element.find(selector).text.strip()

def get_tag_all(element, selector):
  return [e.text.strip() for e in element.find_all(selector)]

async def download_image(img_url, img_path):
  if not os.path.exists("icons"):
    os.mkdir("icons")

  with requests.get(img_url) as img_data:
    if img_data is not None:
      async with aiof.open(img_path, 'wb') as img:
        await img.write(img_data.content)
        await img.flush()

# URL = "https://pokemondb.net/pokedex/all"
# body = requests.get(URL).content
# soup = BeautifulSoup(body, features="html.parser")
# with open('pages/pokemon.html', 'w') as file:
#   file.write(BeautifulSoup.prettify(soup))

conn = sqlite3.connect('db/pokemon.db')
init_db(conn)

if len(sys.argv) > 1 and sys.argv[1] == "refresh":
	html = ""
	with open('pages/pokemon.html', 'r') as file:
		html = file.read()

	soup = BeautifulSoup(html, features="html.parser")
	pokedex_table = soup.body.find(id="pokedex").find("tbody").find_all("tr")
	print("Length", len(pokedex_table))

	for idx, pokemon in enumerate(pokedex_table):
		num, name, elements, total, hp, attack, defense, sp_att, sp_def, speed = pokemon.find_all("td")
		
		# Get small subtitle name
		name_small_element = pokemon.find("small")
		sub_name = ""
		if name_small_element is not None and len(name_small_element) > 0:
			sub_name = name_small_element.text.strip()

		elements = [e.lower() for e in get_tag_all(elements, "a")]
		name = get_tag(name, "a").lower()
		
		img_url = num.find("picture").find("img")["src"]
		img_path = f"icons/{name}.png"

		loop.run_until_complete(download_image(img_url, img_path))

		new_pokemon = Pokemon(
			int(get_tag(num, "span")), 
			name, sub_name, img_path,
			int(total.text.strip()),
			int(hp.text.strip()),
			int(attack.text.strip()),
			int(defense.text.strip()),
			int(sp_att.text.strip()),
			int(sp_def.text.strip()),
			int(speed.text.strip())
		)

		print(f"Adding {new_pokemon.to_tuple()} - {elements} to database")
		add_pokemon_to_database(new_pokemon, elements, conn)

else:
  element_type = sys.argv[1].strip()
  cursor = conn.cursor()
  rows = cursor.execute("""
    SELECT p.number, p.name || " " || p.sub_name as 'full name', GROUP_CONCAT(pt.element_name, ","), 
      p.attack, p.defense, p.special_attack, p.special_defense, p.speed, p.hp
    FROM pokemon as p
    JOIN pokemon_type as pt ON pt.pokemon_number = p.number AND pt.pokemon_name = p.name AND pt.pokemon_sub_name = p.sub_name
    GROUP BY p.number, p.name, p.sub_name
    ORDER BY MAX(p.hp) ASC LIMIT 50
  """).fetchall()

  print(f"All {len(rows)} {element_type} types")
  print(tabulate(rows, headers=['#', 'Name', 'Elements', 'Att', 'Def', 'Sp.Att.', 'Sp.Def.', 'Speed', 'HP'], tablefmt='pretty', stralign='left'))

  cursor.close()

conn.close()