class EV:
	def __init__(self, ev_name, pokemon_name, amount):
		self.ev_name = ev_name
		self.pokemon_name = pokemon_name
		self.amount = amount

	def to_tuple(self):
		return (self.ev_name, self.pokemon_name, self.amount)