CREATE TABLE IF NOT EXISTS pokemon_evs (
	ev_name VARCHAR(64),
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),
	pokemon_number INTEGER,
	ev_amount INTEGER NOT NULL,

	FOREIGN KEY (ev_name) REFERENCES evs(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (ev_name, pokemon_name, pokemon_sub_name, pokemon_number)
)