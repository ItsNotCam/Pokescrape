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
	# for ev in evs:
	# 	cursor.execute("""
	# 		INSERT OR IGNORE INTO pokemon_evs (
	# 			ev_name, pokemon_number, pokemon_name, pokemon_sub_name
	# 		) VALUES (
	# 			?, ?, ?, ?
	# 		)
	# 	""", (ev, pokemon.number, pokemon.name, pokemon.sub_name))

	conn.commit()
	cursor.close()

def init_db(conn):
	cursor = conn.cursor()
	sql_files = [f for f in os.listdir("db") if ".sql" in f]
	for sql_file in sql_files:
		with open(f'db/{sql_file}') as sql:
			cursor.execute(sql.read())
	conn.commit()
	cursor.close()