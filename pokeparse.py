import argparse, sqlite3, os

import get_all_data as GetData
from scrape_pokemon import scrape
from lib import db as DB

def init():
	if not os.path.exists("icons"):
		os.mkdir("icons")
	if not os.path.exists("images"):
		os.mkdir("images")
	if not os.path.exists("pages"):
		os.mkdir("pages")
	if not os.path.exists("pages/pokemon"):
		os.mkdir("pages/pokemon")
	if not os.path.exists("db"):
		os.mkdir("db")

	conn = sqlite3.connect("db/pokemon.db")
	DB.init_db(conn)
	conn.close()

def main():
	init()

	parser = argparse.ArgumentParser(description='Description of your script.')

	parser.add_argument('-p', '--pokemon', action='store_true', help='Get Pokemon')
	parser.add_argument('-ps', '--pstart', type=int, help='The pokemon number to start at')
	parser.add_argument('-pe','--pend', type=int, help='The pokemon number to end at')

	parser.add_argument('-m', '--moves', action='store_true', help='Get Moves')
	parser.add_argument('-a', '--abilities', action='store_true', help='Get Abilities')
	parser.add_argument('-icons', action='store_true', help='Download Icons')
	parser.add_argument('-images', action='store_true', help='Download Images')

	args = parser.parse_args()

	if args.moves:
		GetData.get_all_moves()
	
	if args.abilities:
		GetData.get_all_abilities()
	
	if args.pokemon:
		start_number = args.pstart or None
		end_number = args.pend or None
		scrape(args.icons, args.images, start_number, end_number)

if __name__ == '__main__':
	main()