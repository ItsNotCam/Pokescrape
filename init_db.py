import sqlite3

def init_db(conn):
	cursor = conn.cursor()
	create_pokemon = """
		CREATE TABLE IF NOT EXISTS pokemon (
			number INTEGER NOT NULL,
			name VARCHAR(255) NOT NULL,
			sub_name VARCHAR(255),
			icon_path VARCHAR(255) NOT NULL DEFAULT 'icons/default.png',
			total INTEGER NOT NULL,
			hp INTEGER NOT NULL,
			attack INTEGER NOT NULL,
			defense INTEGER NOT NULL,
			special_attack INTEGER NOT NULL,
			special_defense INTEGER NOT NULL,
			speed INTEGER NOT NULL,

			PRIMARY KEY (number, name, sub_name)
		)
	"""
	cursor.execute(create_pokemon)
	conn.commit()

	create_type = """
		CREATE TABLE IF NOT EXISTS elements (
			name VARCHAR(255) PRIMARY KEY
		)
	"""
	cursor.execute(create_type)
	conn.commit()


	create_p_type = """
		CREATE TABLE IF NOT EXISTS pokemon_type (
			pokemon_number INTEGER,
			pokemon_name VARCHAR(255),
			pokemon_sub_name VARCHAR(255),
			element_name VARCHAR(255),
			
			FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
			FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
			FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),
			FOREIGN KEY (element_name) REFERENCES elements(name),

			PRIMARY KEY (pokemon_number, pokemon_name, pokemon_sub_name, element_name)
		)
	"""
	cursor.execute(create_p_type)
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