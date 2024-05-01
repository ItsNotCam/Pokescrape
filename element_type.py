class Element_Type():
	def __init__(self, pokemon_number, pokemon_type):
		self.pokemon_number = pokemon_number
		self.pokemon_type = pokemon_type

	def to_tuple(self):
		return (self.pokemon_number, self.pokemon_type)