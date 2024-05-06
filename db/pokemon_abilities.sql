CREATE TABLE IF NOT EXISTS pokemon_abilities (
	ability_name VARCHAR(64),
	pokemon_number INTEGER,
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),

	FOREIGN KEY (ability_name) REFERENCES abilities(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (ability_name, pokemon_number, pokemon_name, pokemon_sub_name)
)