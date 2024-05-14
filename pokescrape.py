import argparse, mysql.connector

import lib.get_data as get_data
from lib.scrape import scrape_pokemon
from lib import db as DB

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
		get_data.get_all_moves(conn)
	
	if args.abilities:
		get_data.get_all_abilities(conn)

	if args.damage:
		get_data.get_dmg_effectiveness(conn)
	
	if args.pokemon:
		start_number = args.pstart or None
		end_number = args.pend or None
		verbose = args.verbose or False
		scrape_pokemon(args.icons, args.images, start_number, end_number, verbose, conn)
	
	conn.close()

if __name__ == '__main__':
	main()