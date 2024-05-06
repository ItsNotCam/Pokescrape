class Pokemon:
	def __init__(self, number, name, sub_name, icon_path, total, \
							hp, attack, defense, special_attack, special_defense, \
							speed, species, height, weight
		,catch_rate_number
		,catch_rate_percent
		,friendship_number
		,friendship_extremity
		,base_exp
		,growth_rate

		,gender_male_percent
		,gender_female_percent
		,egg_cycles_number
		,egg_cycles_step_min
		,egg_cycles_step_max):
		self.weight = weight
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

		self.species = species
		self.height = height
		self.catch_rate_number = catch_rate_number
		self.catch_rate_percent = catch_rate_percent
		self.friendship_number = friendship_number
		self.friendship_extremity = friendship_extremity
		self.base_exp = base_exp
		self.growth_rate = growth_rate

		self.gender_male_percent = gender_male_percent
		self.gender_female_percent = gender_female_percent
		self.egg_cycles_number = egg_cycles_number
		self.egg_cycles_step_min = egg_cycles_step_min
		self.egg_cycles_step_max = egg_cycles_step_max
	
	def to_tuple(self):
		return (
			self.number,
		 	self.name,
		 	self.sub_name,
		 	self.icon_path,
		 	self.total,
		 	self.hp,
		 	self.attack,
		 	self.defense,
		 	self.special_attack,
		 	self.special_defense,
		 	self.speed,
			self.species,
			self.height,
			self.weight
		,self.catch_rate_number
		,self.catch_rate_percent
		,self.friendship_number
		,self.friendship_extremity
		,self.base_exp
		,self.growth_rate
		,self.gender_male_percent
		,self.gender_female_percent
		,self.egg_cycles_number
		,self.egg_cycles_step_min
		,self.egg_cycles_step_max
		)
	
	def print(self):
		print("#", self.number)
		print("Name:", self.name)
		print("Sub Name:", self.sub_name)
		print("Img Path:", self.icon_path)
		print("Total:", self.total)
		print("HP:", self.hp)
		print("Att:", self.attack)
		print("Def:", self.defense)
		print("Sp. Att:", self.special_attack)
		print("Sp. Def:", self.special_defense)
		print("Speed:", self.speed)
		print("Height:", self.height)
		# print("EVs:", self.ev_amounts, self.ev_types)
		print("Catch Rates:", f"{self.catch_rate_number} - {self.catch_rate_percent}%")
		print("Friendship:", f"{self.friendship_number} ({self.friendship_extremity})")
		print("EXP:", self.base_exp)
		print("Growth Rate:", self.growth_rate)
		print("Gender:", f"{self.gender_male_percent}% male, {self.gender_female_percent}% female")
		print("Egg Cycles:" f"{self.egg_cycles_number} ({self.egg_cycles_step_min}-{self.egg_cycles_step_max})")