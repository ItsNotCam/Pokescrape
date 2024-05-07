import os

def init_db(conn):
	cursor = conn.cursor()
	sql_files = [f for f in os.listdir("db") if ".sql" in f]
	for sql_file in sql_files:
		with open(f'db/{sql_file}') as sql:
			cursor.execute(sql.read())
	conn.commit()
	cursor.close()
	return conn
    
def entity_exists(SQL, VARS, conn):
	cursor = conn.cursor()
	cursor.execute(SQL, VARS)
	result = cursor.fetchone()
	cursor.close()
	return result is not None and result[0] > 0

def add_ability_to_database(ability, conn):
	conn.execute("INSERT OR IGNORE INTO abilities (name, description, generation) VALUES (?,?,?)", ability.to_tuple())
	conn.commit()

def add_element_to_database(element, conn):
	if not entity_exists("SELECT COUNT(*) FROM elements WHERE name=?", (element,), conn):
		conn.execute("INSERT OR IGNORE INTO elements VALUES (?)", (element, ))
		conn.commit()

def add_pokemon_type_to_database(pokemon, element, conn):
	vars = (pokemon.number, pokemon.name, pokemon.sub_name, element)
	exists = entity_exists("""
		SELECT COUNT(*) FROM pokemon_elements WHERE pokemon_number=? AND pokemon_name=? AND pokemon_sub_name=? AND element_name=?""", 
		vars, conn
	)

	if not exists:
		conn.execute("INSERT OR IGNORE INTO pokemon_elements VALUES (?,?,?,?)", vars)
		conn.commit()

def add_pokemon_to_database(pokemon, elements, abilities, conn):
	# ev_amount, ev_type,
	cursor = conn.cursor()
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
	conn.commit()

	for element in elements:
		add_element_to_database(element, conn)
		add_pokemon_type_to_database(pokemon, element, conn)
	
	cursor.close()

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

def get_and_add_evs_to_database(pokemon, soup2, conn):
		ev_selection = soup2.select("th:-soup-contains('EV yield') + td")
		if len(ev_selection) > 0:
			ev_list = ev_selection[0].get_text(strip=True).split(", ")
			for ev in ev_list:
				ev_split = ev.split(" ")
				amount = int(ev_split[0])
				name = "_".join(ev_split[1::])

				ev_sql = "INSERT OR IGNORE INTO evs VALUES (?)"
				ev_vals = (name,)
				conn.execute(ev_sql, ev_vals)

				conn.commit()

				pkmn_ev_sql = "INSERT OR IGNORE INTO pokemon_evs VALUES (?,?,?,?,?)"
				pkmn_ev_vals = (name, pokemon.name, pokemon.sub_name, pokemon.number, amount)
				conn.execute(pkmn_ev_sql, pkmn_ev_vals)

def add_moves_to_database(pokemon, MOVES, conn):
	print(MOVES)
	level_up_moveset, egg_moveset, tm_moveset = MOVES

	def insert_move(source, move):
		conn.execute("""
			INSERT OR IGNORE INTO pokemon_moves (
				source, move_name, pokemon_name, pokemon_sub_name, pokemon_number, level
			) VALUES (
				?, ?, ?, ?, ?, ?
			)
		""", (source, move[0], pokemon.name, pokemon.sub_name, pokemon.number, move[1]))

	for move in level_up_moveset:
		insert_move("level_up", move)

	for move in egg_moveset:
		insert_move("egg", move)

	for move in tm_moveset:
		insert_move("tm", move)