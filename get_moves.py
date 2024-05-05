from bs4 import BeautifulSoup
import requests, sys, json, sqlite3
from dbops import init_db

from dbops import add_move_to_database
from objects.move import Move

from tabulate import tabulate

def get_tag(element, selector):
  return element.find(selector).text.strip()

def to_number(str):
	if str.isdigit():
		return int(str)
	return None	

def scrape(start_index):
	URL = "https://pokemondb.net/move/all"
	body = requests.get(URL).content
	soup = BeautifulSoup(body, features="html.parser")
	with open('pages/moves.html', 'w') as file:
		file.write(BeautifulSoup.prettify(soup))

	html = ""
	with open('pages/moves.html', 'r') as file:
		html = file.read()

	soup = BeautifulSoup(html, features="html.parser")
	moves = soup.body.find(id="moves").find("tbody").find_all("tr")
	moves = moves[start_index:]

	if sys.argv[1] == "refresh":
		for idx, move in enumerate(moves):
			name, element, dmg_category, power, accuracy, pp, description, probability = move.find_all("td")

			dmg_cat_img = dmg_category.find("img")
			if dmg_cat_img is not None:
				dmg_category = dmg_cat_img["alt"]	
			else:
				dmg_category = "-"

			new_move = Move(
				get_tag(name, "a"), 
				get_tag(element, "a"), 
				dmg_category, 		
				to_number(power.text.strip()),
				to_number(accuracy.text.strip()),
				to_number(pp.text.strip()),
				description.text.strip(),
				to_number(probability.text.strip())
			)

			print(idx, new_move.to_tuple())
			add_move_to_database(new_move, sqlite3.connect('db/pokemon.db'))

# else:
#   element_type = sys.argv[1].strip()
#   cursor = conn.cursor()
#   rows = cursor.execute("""
#     SELECT name, element_name, power, accuracy
#     FROM moves
#     WHERE element_name=?
#     LIMIT 25
#   """, (sys.argv[1],)).fetchall()

#   print(f"All {len(rows)} {element_type} types")
#   print(tabulate(rows, headers=['name', 'element', 'power', 'accuracy'], tablefmt='pretty', stralign='left'))
