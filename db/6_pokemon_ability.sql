CREATE TABLE IF NOT EXISTS pokemon_ability (
	ability_name VARCHAR(64),
	pokemon_number INTEGER,
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),

	FOREIGN KEY (ability_name) REFERENCES ability(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (ability_name, pokemon_number, pokemon_name, pokemon_sub_name)
);
CREATE INDEX idx_ability_name ON pokemon_ability (ability_name);
CREATE INDEX idx_ability_pokemon_number ON pokemon_ability (pokemon_number);
CREATE INDEX idx_ability_pokemon_name ON pokemon_ability (pokemon_name);
CREATE INDEX idx_ability_pokemon_sub_name ON pokemon_ability (pokemon_sub_name);