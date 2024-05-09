import os

def add_pokemon_to_database(pokemon, abilities, elements, moves, evs, conn):
	cursor = conn.cursor()

	# Add pokemon
	cursor.execute("""
		INSERT OR IGNORE INTO pokemon (
			number, name, sub_name, icon_path, total, hp, attack, defense, special_attack, special_defense, speed,
			species, height, weight, catch_rate_num, catch_rate_percent, friendship_num,
			friendship_extremity, base_exp, growth_rate, gender_male_percent, gender_female_percent, egg_cycles_num,
			egg_cycles_steps_min, egg_cycles_steps_max
		) VALUES (
			?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
			?, ?, ?, ?, ?, ?
		)
	""", pokemon.to_tuple())

	# Add abilities
	for ability in abilities:
		cursor.execute("""
			INSERT OR IGNORE INTO pokemon_abilities (
				ability_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				?, ?, ?, ?
			)
		""", (ability, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add elements
	for element in elements:
		cursor.execute("""
			INSERT OR IGNORE INTO pokemon_elements (
				element_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				?, ?, ?, ?
			)
		""", (element, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add moves
	for move in moves:
		cursor.execute("""
			INSERT OR IGNORE INTO pokemon_moves (
				source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
			) VALUES (
				?, ?, ?, ?, ?, ?
			)
		""", (move.source, move.move_name, pokemon.number, pokemon.name, pokemon.sub_name, move.level))
	
	# Add evs
	for ev in evs:
		cursor.execute("""
			INSERT OR IGNORE INTO pokemon_evs (
				ev_name, pokemon_number, pokemon_name, pokemon_sub_name, ev_amount
			) VALUES (
				?, ?, ?, ?, ?
			)
		""", ev.to_tuple())

	conn.commit()
	cursor.close()

def init_db(conn):
	cursor = conn.cursor()
	sql_files = [f for f in os.listdir("db") if ".sql" in f]
	for sql_file in sql_files:
		with open(f'db/{sql_file}') as sql:
			print("Reading from", sql_file)
			cursor.executescript(sql.read())
	conn.commit()
	cursor.close()

def add_moves_to_database(pokemon, MOVES, conn):
	level_up_moveset, egg_moveset, tm_moveset = MOVES

	def insert_move(source, move):
		conn.execute("""
			INSERT OR IGNORE INTO pokemon_moves (
				source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
			) VALUES (
				?, ?, ?, ?, ?, ?
			)
		""", (source, move[0], pokemon.number, pokemon.name, pokemon.sub_name, move[1]))

	for move in level_up_moveset:
		insert_move("Level Up", move)

	for move in egg_moveset:
		insert_move("Egg", move)

	for move in tm_moveset:
		insert_move("TM", move)
		
def add_move_to_database(move, conn):
	add_element_to_database(move.element_name, conn)
	conn.execute("""
		INSERT OR IGNORE INTO moves (
			name, element_name, dmg_category, power, accuracy, pp, description, probability
		) VALUES (
			?,?,?,?,?,?,?,?
		)
	""", move.to_tuple())
	conn.commit()

def add_ability_to_database(ability, conn):
	conn.execute("INSERT OR IGNORE INTO abilities (name, description, generation) VALUES (?,?,?)", ability.to_tuple())
	conn.commit()

def add_element_to_database(element, conn):
	conn.execute("INSERT OR IGNORE INTO elements VALUES (?)", (element, ))
	conn.commit()

def add_dmg_effectiveness(dmg_src, dmg_dest, effect, conn):
	conn.execute("""
		INSERT OR IGNORE INTO move_effectiveness (
			dmg_source, dmg_dest, effectiveness
		) VALUES (
			?,?,?
		)
	""", (dmg_src, dmg_dest, effect))
	conn.commit()