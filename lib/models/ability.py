class Ability:
	def __init__(self, name, description, generation):
		self.name = name
		self.description = description
		self.generation = generation

	def to_tuple(self):
		return (self.name, self.description, self.generation)