import argparse, sqlite3, os

from get_moves import scrape as scrape_moves
from get_pokemon import scrape as scrape_pokemon
from dbops import init_db

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

	init_db(sqlite3.connect("db/pokemon.db"))

def main():
	init()

	parser = argparse.ArgumentParser(description='Description of your script.')
	parser.add_argument('-pokemon', type=int, help='Get Pokemon')
	parser.add_argument('-moves', type=int, help='Get Moves')
	parser.add_argument('-imgs', action='store_true', help='Download images')

	args = parser.parse_args()

	if args.pokemon:
		scrape_pokemon(download_images=args.imgs, start_index=args.pokemon)
	if args.moves:
		scrape_moves(args.moves)

if __name__ == '__main__':
	main()