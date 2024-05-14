CREATE TABLE IF NOT EXISTS pokemon_move (
	id SERIAL UNIQUE PRIMARY KEY,
	source VARCHAR(64) NOT NULL,
	pokemon_number INTEGER,
	move_name VARCHAR(64) NOT NULL,
	pokemon_name VARCHAR(64) NOT NULL,
	pokemon_sub_name VARCHAR(64) NOT NULL,
	level INTEGER,

	CONSTRAINT fk_move
	FOREIGN KEY (move_name)
	REFERENCES move(name),

	CONSTRAINT fk_pokemon_move FOREIGN KEY (
		pokemon_number, pokemon_name, pokemon_sub_name
	) REFERENCES pokemon (
		number, name, sub_name
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pokemon_move_partial
ON pokemon_move (id)
WHERE id IS NOT NULL;

