class PokemonMove:
	def __init__(self, source=None, move_name=None, level=None):
		self.source = source
		self.move_name = move_name
		self.level = level

	def to_tuple(self):
		return (self.source, self.move_name, self.level)