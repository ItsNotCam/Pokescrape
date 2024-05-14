CREATE TABLE IF NOT EXISTS pokemon_move (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	source VARCHAR(64) NOT NULL,
	pokemon_number INTEGER,
	move_name VARCHAR(64) NOT NULL,
	pokemon_name VARCHAR(64) NOT NULL,
	pokemon_sub_name VARCHAR(64) NOT NULL,
	level INTEGER,

	FOREIGN KEY (move_name) REFERENCES move(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name)
);

CREATE INDEX idx_move_name ON pokemon_move (move_name);
CREATE INDEX idx_moves_pokemon_number ON pokemon_move (pokemon_number);
CREATE INDEX idx_moves_pokemon_name ON pokemon_move (pokemon_name);
CREATE INDEX idx_moves_pokemon_sub_name ON pokemon_move (pokemon_sub_name);
