class Element:
	def __init__(self, name):
		self.name = name
	
	def to_tuple(self):
		return (self.name,)