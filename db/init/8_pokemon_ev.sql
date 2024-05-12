CREATE TABLE IF NOT EXISTS pokemon_ev (
	ev_name VARCHAR(64),
	ev_amount INTEGER NOT NULL,
	pokemon_number INTEGER,
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),

	FOREIGN KEY (ev_name) REFERENCES ev(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (ev_name, pokemon_number, pokemon_name, pokemon_sub_name)
);

CREATE INDEX idx_ev_name ON pokemon_ev (ev_name);
CREATE INDEX idx_evs_pokemon_number ON pokemon_ev (pokemon_number);
CREATE INDEX idx_evs_pokemon_name ON pokemon_ev (pokemon_name);
CREATE INDEX idx_evs_pokemon_sub_name ON pokemon_ev (pokemon_sub_name);