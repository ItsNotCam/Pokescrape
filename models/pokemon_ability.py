class PokemonAbility:
	def __init__(self, ability_name, pokemon_number, pokemon_name, pokemon_sub_name):
		self.ability_name = ability_name
		self.pokemon_number = pokemon_number
		self.pokemon_name = pokemon_name
		self.pokemon_sub_name = pokemon_sub_name
	
	def to_tuple(self):
		return (self.ability_name, self.pokemon_number, self.pokemon_name, self.pokemon_sub_name)