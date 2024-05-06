class PokemonMove:
	def __init__(self):
		self.id = 0
		self.source = ""
		self.move_name = ""
		self.pokemon_name = ""
		self.pokemon_sub_name = ""
		self.pokemon_number = ""
		self.level = 0

	def get_moves_from_soup(self, soup):
		level_up_moves_soup = soup.find(text="Moves learnt by level up")\
			.parent.parent.select("tbody tr")
		egg_moves_soup = soup.find(text="Egg moves")\
			.parent.parent.select("tbody tr")
		tm_moves_soup = soup.find(text="Moves learnt by TM")\
			.parent.parent.select("tbody tr")
		
		level_up_moves = []
		egg_moves = []
		tm_moves = []
		
		for m in level_up_moves_soup:
			name = m.find("a").get_text(strip=True)
			level = m.find_all("td")[0].get_text()
			level_up_moves.append((name, level))

		for m in egg_moves_soup:
			name = m.find("a").get_text(strip=True)
			level_up_moves.append((name, -1))

		for m in tm_moves_soup:
			name = ""
			name_soup = m.find_all("a")
			if name_soup:
				name = name_soup[1].get_text(strip=True)
			
			level_up_moves.append((name, -1))

		return [level_up_moves, egg_moves, tm_moves]