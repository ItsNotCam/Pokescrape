import argparse, sqlite3, os

from get_pokemon import scrape
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
	parser.add_argument('-pokemon', type=int, help='Get Pokemon')
	parser.add_argument('-moves', type=int, help='Get Moves')
	parser.add_argument('-imgs', action='store_true', help='Download images')

	args = parser.parse_args()

	scrape(download_images=args.imgs, start_index=args.pokemon)
	# if args.pokemon:
	# 	scrape_pokemon(download_images=args.imgs, start_index=args.pokemon)
	# if args.moves:
	# 	scrape_moves(args.moves)

if __name__ == '__main__':
	main()