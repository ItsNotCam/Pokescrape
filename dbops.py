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

def add_element_to_database(element, conn):
	if not entity_exists("SELECT COUNT(*) FROM elements WHERE name=?", (element,), conn):
		conn.execute("INSERT INTO elements VALUES (?)", (element, ))
		conn.commit()

def add_pokemon_type_to_database(pokemon, element, conn):
	vars = (pokemon.number, pokemon.name, pokemon.sub_name, element)
	exists = entity_exists("""
		SELECT COUNT(*) FROM pokemon_type WHERE pokemon_number=? AND pokemon_name=? AND pokemon_sub_name=? AND element_name=?""", 
		vars, conn
	)

	if not exists:
		conn.execute("INSERT INTO pokemon_type VALUES (?,?,?,?)", vars)
		conn.commit()

def add_pokemon_to_database(pokemon, elements, conn):
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO pokemon (
			number, name, sub_name, icon_path, total, hp, attack, defense, special_attack, special_defense, speed
		) VALUES (
			?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
		)
	""", pokemon.to_tuple())
	conn.commit()

	for element in elements:
		add_element_to_database(element, conn)
		add_pokemon_type_to_database(pokemon, element, conn)

	cursor.close()

def add_move_to_database(move, conn):
	add_element_to_database(move.element, conn)
	conn.execute("""
		INSERT INTO moves (
			name, element_name, dmg_category, power, accuracy, pp, description, probability
		) VALUES (
			?,?,?,?,?,?,?,?
		)
	""", move.to_tuple())
	conn.commit()
