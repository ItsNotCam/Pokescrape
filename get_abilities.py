import requests, sqlite3
from dbops import init_db
from bs4 import BeautifulSoup
from tabulate import tabulate

body = requests.get("https://pokemondb.net/ability").content
soup = BeautifulSoup(body, features="html.parser")

conn = sqlite3.connect("db/pokemon.db")
init_db(conn)

abilities = soup.select("#abilities tbody tr")
for ability in abilities:
	name, _, description, generation = [r.get_text(strip=True) for r in ability.select("td")]
	conn.execute("INSERT OR IGNORE INTO abilities VALUES (?,?,?)", (name, description, generation))

results = conn.execute("SELECT * FROM abilities").fetchall()
print(tabulate(results, headers=['name', 'description', 'generation'], tablefmt='pretty', stralign='left'))
