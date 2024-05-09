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
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_move_name ON pokemon_moves (move_name);
CREATE INDEX IF NOT EXISTS idx_moves_pokemon_number ON pokemon_moves (pokemon_number);
CREATE INDEX IF NOT EXISTS idx_moves_pokemon_name ON pokemon_moves (pokemon_name);
CREATE INDEX IF NOT EXISTS idx_moves_pokemon_sub_name ON pokemon_moves (pokemon_sub_name);
