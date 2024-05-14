import os, psycopg2
from dotenv import load_dotenv

def update_pokemon_image_path(pokemon_number, pokemon_name, pokemon_sub_name, img_link, conn):
	with conn.cursor() as cursor:
		cursor.execute("""
			UPDATE pokemon SET icon_path=%s
			WHERE number=%s AND name=%s AND sub_name=%s
		""", (img_link, pokemon_number, pokemon_name, pokemon_sub_name))

def add_pokemon_to_database(pokemon, abilities, elements, moves, evs, conn):
	cursor = conn.cursor()

	# Add pokemon
	cursor.execute("""
		INSERT INTO pokemon (
			number, name, sub_name, icon_path, total, hp, attack, defense, special_attack, special_defense, speed,
			species, height, weight, catch_rate_num, catch_rate_percent, friendship_num,
			friendship_extremity, base_exp, growth_rate, gender_male_percent, gender_female_percent, egg_cycles_num,
			egg_cycles_steps_min, egg_cycles_steps_max
		) VALUES (
			%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s, %s
		) ON CONFLICT (
			number, name, sub_name
		) DO NOTHING;
	""", pokemon.to_tuple())

	for ev in evs:
		cursor.execute("""
			INSERT INTO ev (
				name
			) VALUES (
				%s
			) ON CONFLICT (
				name
			) DO NOTHING;
		""", (ev.ev_name, ))

		cursor.execute("""
			INSERT INTO pokemon_ev (
				ev_name, ev_amount, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s, %s
			) ON CONFLICT (
				ev_name, pokemon_number, pokemon_name, pokemon_sub_name
			) DO NOTHING;
		""", ev.to_tuple())

	# Add abilities
	for ability in abilities:
		cursor.execute("""
			INSERT INTO pokemon_ability (
				ability_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s
			) ON CONFLICT (
				ability_name, pokemon_number, pokemon_name, pokemon_sub_name
			) DO NOTHING;
		""", (ability, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add elements
	for element in elements:
		cursor.execute("""
			INSERT INTO pokemon_element (
				element_name, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s
			) ON CONFLICT (
				element_name, pokemon_number, pokemon_name, pokemon_sub_name
			) DO NOTHING;
		""", (element, pokemon.number, pokemon.name, pokemon.sub_name))
	
	# Add moves
	for move in moves:
		cursor.execute("""
			INSERT INTO pokemon_move (
				source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
			) VALUES (
				%s, %s, %s, %s, %s, %s
			);
		""", (move.source, move.move_name, pokemon.number, pokemon.name, pokemon.sub_name, move.level))
	
	# Add evs
	for ev in evs:
		cursor.execute("""
			INSERT INTO pokemon_ev (
				ev_name, ev_amount, pokemon_number, pokemon_name, pokemon_sub_name
			) VALUES (
				%s, %s, %s, %s, %s
			) ON CONFLICT (
				ev_name, pokemon_number, pokemon_name, pokemon_sub_name
			) DO NOTHING;
		""", ev.to_tuple())

	cursor.close()

def connect(autocommit=True):
	load_dotenv()

	conn = psycopg2.connect(
		dbname=os.getenv("DB_NAME"),
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASS"),
		host=os.getenv("DB_HOST"),
		port=os.getenv("DB_PORT")
	)
	conn.autocommit = autocommit
	return conn

def init_db():
	conn = connect()

	sql_files = sorted([f for f in os.listdir("db") if ".sql" in f])
	print("Getting SQL from files")
	with conn.cursor() as cursor:
		for sql_file in sql_files:
			file_name = f'db/{sql_file}'
			with open(file_name) as sql:
				print(file_name)
				data = sql.read()
				data = data.split(";")[:-1]
				for command in data:
					print(command)
					cursor.execute(command)
	
	return conn

def add_moves_to_database(pokemon, MOVES, conn):
	level_up_moveset, egg_moveset, tm_moveset = MOVES

	def insert_move(source, move):
		with conn.cursor() as cursor:
			cursor.execute("""
				INSERT INTO pokemon_move (
					source, move_name, pokemon_number, pokemon_name, pokemon_sub_name, level
				) VALUES (
					%s, %s, %s, %s, %s, %s
				) ON CONFLICT (
					move_name, pokemon_number, pokemon_name, pokemon_sub_name
				) DO NOTHING;
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
			INSERT INTO move (
				name, element_name, dmg_category, power, accuracy, pp, description, probability
			) VALUES (
				%s, %s, %s, %s, %s, %s, %s, %s
			) ON CONFLICT (
				name
			) DO NOTHING;
		"""
		values = move.to_tuple()
		cursor.execute(insert_sql, values)

def add_ability_to_database(ability, conn):
	with conn.cursor() as cursor:
		cursor.execute(
			"""INSERT INTO ability (
				name, description, generation
			) VALUES (
				%s,%s,%s
			) ON CONFLICT (
				name
			) DO NOTHING;
			""", 
			ability.to_tuple()
		)

def add_element_to_database(element, conn):
	with conn.cursor() as cursor:
		cursor.execute("""
			INSERT INTO element (
				name
			) VALUES (
				%s
			) ON CONFLICT (
				name
			) DO NOTHING;
		""", (element, ))

def add_dmg_effectiveness(dmg_src, dmg_dest, effect, conn):
	with conn.cursor() as cursor:
		# cursor.execute("""
		# INSERT INTO move_effectiveness (
		# 	dmg_source, dmg_dest, effectiveness
		# ) VALUES (
		# 	%s,%s,%s
		# ) ON CONFLICT (
		# 	dmg_source, dmg_dest
		# ) DO NOTHING;
		# """, (dmg_src, dmg_dest, effect))
		cursor.execute("""
		INSERT INTO move_effectiveness (
			dmg_source, dmg_dest, effectiveness
		) VALUES (
			%s,%s,%s
		) ON CONFLICT (
			dmg_source, dmg_dest
		) DO NOTHING;
		""", (dmg_src, dmg_dest, effect))