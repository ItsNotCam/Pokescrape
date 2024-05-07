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