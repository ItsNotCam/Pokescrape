class PokemonMove:
	def __init__(self, id=-1, source="", move_name="", pokemon_name="", pokemon_sub_name="", pokemon_number=0, level=0):
		self.id = id
		self.source = source
		self.move_name = move_name
		self.pokemon_name = pokemon_name
		self.pokemon_sub_name = pokemon_sub_name
		self.pokemon_number = pokemon_number
		self.level = level

	def to_tuple(self):
		return (self.id, self.source, self.move_name, self.pokemon_name, self.pokemon_sub_name, self.pokemon_number, self.level)