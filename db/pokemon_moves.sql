CREATE TABLE IF NOT EXISTS pokemon_moves (
	id INTEGER PRIMARY KEY,
	source VARCHAR(64) NOT NULL,
	pokemon_number VARCHAR(64),
	move_name VARCHAR(64) NOT NULL,
	pokemon_name VARCHAR(64) NOT NULL,
	pokemon_sub_name VARCHAR(64) NOT NULL,
	level INTEGER,

	FOREIGN KEY (move_name) REFERENCES moves(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name)
)