class Move:
	def __init__(self, name, element_name, dmg_category, power, accuracy, pp, description, probability):
		self.name = name
		self.element_name = element_name
		self.dmg_category = dmg_category
		self.power = power
		self.accuracy = accuracy
		self.pp = pp
		self.description = description
		self.probability = probability

	def to_tuple(self):
		return (
			self.name,
			self.element_name,
			self.dmg_category,
			self.power,
			self.accuracy,
			self.pp,
			self.description,
			self.probability,
		)