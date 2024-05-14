CREATE TABLE IF NOT EXISTS pokemon_ev (
	ev_name VARCHAR(64),
	ev_amount INTEGER NOT NULL,
	pokemon_number INTEGER,
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),

	CONSTRAINT fk_ev
	FOREIGN KEY (ev_name) 
	REFERENCES ev(name),
	
	CONSTRAINT fk_pokemon_ev 
	FOREIGN KEY (
		pokemon_number, pokemon_name, pokemon_sub_name
	) REFERENCES pokemon (
		number, name, sub_name
	),

	PRIMARY KEY (
		ev_name, pokemon_number, pokemon_name, pokemon_sub_name
	)	
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pokemon_ev_partial
ON pokemon_ev (
	ev_name, pokemon_number, pokemon_name, pokemon_sub_name
)
WHERE ev_name IS NOT NULL 
	AND pokemon_number IS NOT NULL 
	AND pokemon_name IS NOT NULL
	AND pokemon_sub_name IS NOT NULL;
