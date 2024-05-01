class Pokemon:
	def __init__(self, number, name, sub_name, icon_path, total, hp, attack, defense, special_attack, special_defense, speed):
		self.number = number
		self.name = name
		self.sub_name = sub_name
		self.icon_path = icon_path
		self.total = total
		self.hp = hp
		self.attack = attack
		self.defense = defense
		self.special_attack = special_attack
		self.special_defense = special_defense
		self.speed = speed
	
	def to_tuple(self):
		return (self.number,
		 self.name,
		 self.sub_name,
		 self.icon_path,
		 self.total,
		 self.hp,
		 self.attack,
		 self.defense,
		 self.special_attack,
		 self.special_defense,
		 self.speed)