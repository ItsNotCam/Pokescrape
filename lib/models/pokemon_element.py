class PokemonElement:
	def __init__(self, element_name, pokemon_number, pokemon_name, pokemon_sub_name):
		self.element_name = element_name
		self.pokemon_number = pokemon_number
		self.pokemon_name = pokemon_name
		self.pokemon_sub_name = pokemon_sub_name
	
	def to_tuple(self):
		return (self.element_name, self.pokemon_number, self.pokemon_name, self.pokemon_sub_name)