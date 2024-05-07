class Pokemon:
	def __init__(self, number, name, sub_name, icon_path, stats_data, physical_data, training_data, breeding_data):
		self.number = number
		self.name = name
		self.sub_name = sub_name
		self.icon_path = icon_path
		self.stats = stats_data
		self.physical_data = physical_data
		self.training_data = training_data
		self.breeding_data = breeding_data
	
	def to_tuple(self):
		return (
			self.number,
		 	self.name,
		 	self.sub_name,
		 	self.icon_path,
			 
		 	self.stats.total,
		 	self.stats.hp,
		 	self.stats.attack,
		 	self.stats.defense,
		 	self.stats.special_attack,
		 	self.stats.special_defense,
		 	self.stats.speed,
			 
			self.physical_data.species,
			self.physical_data.height,
			self.physical_data.weight,

			self.training_data.catch_rate_number,
			self.training_data.catch_rate_percent,
			self.training_data.friendship_number,
			self.training_data.friendship_extremity,
			self.training_data.base_exp,
			self.training_data.growth_rate,

			self.breeding_data.gender_male_percent,
			self.breeding_data.gender_female_percent,
			self.breeding_data.egg_cycles_number,
			self.breeding_data.egg_cycles_steps_min,
			self.breeding_data.egg_cycles_steps_max
		)