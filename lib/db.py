import os, mysql.connector

def add_pokemon_to_database(pokemon, abilities, elements, moves, evs, conn):
	cursor = conn.cursor()

	for ev in evs:
		cursor.execute("""
			INSERT IGNORE INTO ev (
				name
			) VALUES (
				%s
			)
		""", (ev.ev_name, ))

		cursor.execute("""
			INSERT IGNORE INTO pokemon_ev (
				ev_name, ev_amount, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s, %s
			)
		""", ev.to_tuple())

	# Add pokemon
	cursor.execute("""
		INSERT IGNORE INTO pokemon (
			number, name, sub_name, icon_path, total, hp, attack, defense, special_attack, special_defense, speed,
			species, height, weight, catch_rate_num, catch_rate_percent, friendship_num,
			friendship_extremity, base_exp, growth_rate, gender_male_percent, gender_female_percent, egg_cycles_num,
			egg_cycles_steps_min, egg_cycles_steps_max
		) VALUES (
			%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s, %s
		)
	""", pokemon.to_tuple())

	# Add abilities
	for ability in abilities:
		cursor.execute("""
			INSERT IGNORE INTO pokemon_ability (
				ability_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s
			)
		""", (ability, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add elements
	for element in elements:
		cursor.execute("""
			INSERT IGNORE INTO pokemon_element (
				element_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s
			)
		""", (element, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add moves
	for move in moves:
		cursor.execute("""
			INSERT IGNORE INTO pokemon_move (
				source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
			) VALUES (
				%s, %s, %s, %s, %s, %s
			)
		""", (move.source, move.move_name, pokemon.number, pokemon.name, pokemon.sub_name, move.level))
	
	# Add evs
	for ev in evs:
		cursor.execute("""
			INSERT IGNORE INTO pokemon_ev (
				ev_name, pokemon_number, pokemon_name, pokemon_sub_name, ev_amount
			) VALUES (
				%s, %s, %s, %s, %s
			)
		""", ev.to_tuple())

	cursor.close()

def init_db():
	conn = mysql.connector.connect(
		host="localhost",
		user="cam",
		password="ok",
		database="pokemon"
	)

	sql_files = sorted([f for f in os.listdir("db") if ".sql" in f])
	print("Getting SQL from files")
	with conn.cursor() as cursor:
		for sql_file in sql_files:
			file_name = f'db/{sql_file}'
			with open(file_name) as sql:
				print(file_name)
				data = sql.read()
				print(data)
				data = data.split(";")[:-1]
				for command in data:
					cursor.execute(command)
	
	return conn

def add_moves_to_database(pokemon, MOVES, conn):
	level_up_moveset, egg_moveset, tm_moveset = MOVES

	def insert_move(source, move):
		with conn.cursor() as cursor:
			cursor.execute("""
				INSERT IGNORE INTO pokemon_move (
					source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
				) VALUES (
					%s, %s, %s, %s, %s, %s
				)
			""", (source, move[0], pokemon.number, pokemon.name, pokemon.sub_name, move[1]))

	for move in level_up_moveset:
		insert_move("Level Up", move)

	for move in egg_moveset:
		insert_move("Egg", move)

	for move in tm_moveset:
		insert_move("TM", move)
	
def add_move_to_database(move, conn):
	with conn.cursor() as cursor:
		add_element_to_database(move.element_name, conn)
		insert_sql = """
			INSERT IGNORE INTO move (
				name, element_name, dmg_category, power, accuracy, pp, description, probability
			) VALUES (
				%s, %s, %s, %s, %s, %s, %s, %s
			)
		"""
		values = move.to_tuple()
		cursor.execute(insert_sql, values)

def add_ability_to_database(ability, conn):
	with conn.cursor() as cursor:
		cursor.execute(
			"INSERT IGNORE INTO ability (name, description, generation) VALUES (%s,%s,%s)", 
			ability.to_tuple()
		)

def add_element_to_database(element, conn):
	with conn.cursor() as cursor:
		cursor.execute("INSERT IGNORE INTO element (name) VALUES (%s)", (element, ))

def add_dmg_effectiveness(dmg_src, dmg_dest, effect, conn):
	with conn.cursor() as cursor:
		cursor.execute("""
		INSERT IGNORE INTO move_effectiveness (
			dmg_source, dmg_dest, effectiveness
		) VALUES (
			%s,%s,%s
		)
		""", (dmg_src, dmg_dest, effect))