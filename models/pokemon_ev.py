class PokemonEV:
	def __init__(self, ev_name, pokemon_number, pokemon_name, pokemon_sub_name, ev_amount):
		self.ev_name = ev_name
		self.pokemon_number = pokemon_number
		self.pokemon_name = pokemon_name
		self.pokemon_sub_name = pokemon_sub_name
		self.ev_amount = ev_amount
	
	def to_tuple(self):
		return (self.ev_name, self.pokemon_number, self.pokemon_name, self.pokemon_sub_name, self.ev_amount)