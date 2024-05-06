CREATE TABLE IF NOT EXISTS pokemon_moves (
	id INTEGER PRIMARY KEY,
	source VARCHAR(64) NOT NULL,
	move_name VARCHAR(64) NOT NULL,
	pokemon_name VARCHAR(64) NOT NULL,
	pokemon_sub_name VARCHAR(64) NOT NULL,
	pokemon_number VARCHAR(64) NOT NULL,
	level INTEGER NOT NULL,

	FOREIGN KEY (move_name) REFERENCES moves(name),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number)
)