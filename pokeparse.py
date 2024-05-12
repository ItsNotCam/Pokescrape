import argparse, os

import get_all_data as GetData
from scrape_pokemon import scrape
from lib import db as DB

import mysql.connector

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

	# conn = sqlite3.connect("db/pokemon.db")
	return 

def main():
	parser = argparse.ArgumentParser(description='Description of your script.')

	parser.add_argument('--init', action='store_true', help='initialize database')
	parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed debug')

	parser.add_argument('-p', '--pokemon', action='store_true', help='Get Pokemon')
	parser.add_argument('-ps', '--pstart', type=int, help='The pokemon number to start at')
	parser.add_argument('-pe','--pend', type=int, help='The pokemon number to end at')

	parser.add_argument('-m', '--moves', action='store_true', help='Get Moves')
	parser.add_argument('-a', '--abilities', action='store_true', help='Get Abilities')
	parser.add_argument('-d', '--damage', action='store_true', help='Get Damage Effectiveness')

	parser.add_argument('--icons', action='store_true', help='Download Icons')
	parser.add_argument('--images', action='store_true', help='Download Images')

	args = parser.parse_args()

	conn = None
	if args.init:
		conn = DB.init_db()
	else:
		conn = mysql.connector.connect(
			host="localhost",
			user="cam",
			password="ok",
			database="pokemon"
		)

	if args.moves:
		GetData.get_all_moves(conn)
	
	if args.abilities:
		GetData.get_all_abilities(conn)

	if args.damage:
		GetData.get_dmg_effectiveness(conn)
	
	if args.pokemon:
		start_number = args.pstart or None
		end_number = args.pend or None
		verbose = args.verbose or False
		scrape(args.icons, args.images, start_number, end_number, verbose, conn)
	
	conn.close()

if __name__ == '__main__':
	main()