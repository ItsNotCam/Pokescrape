CREATE TABLE IF NOT EXISTS pokemon_ability (
	ability_name VARCHAR(64),
	pokemon_number INTEGER,
	pokemon_name VARCHAR(64),
	pokemon_sub_name VARCHAR(64),

	CONSTRAINT fk_ability_name FOREIGN KEY (ability_name) REFERENCES ability(name),
	CONSTRAINT fk_pokemon_ability FOREIGN KEY (
		pokemon_number, pokemon_name, pokemon_sub_name
	) REFERENCES pokemon(
		number, name, sub_name
	),
	-- CONSTRAINT fk_pokemon_number FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
	-- CONSTRAINT fk_pokemon_name FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
	-- CONSTRAINT fk_pokemon_sub_name FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (
		ability_name, pokemon_number, pokemon_name, pokemon_sub_name
	),

	CONSTRAINT uq_pokemon_ability_constraint UNIQUE (
		ability_name, pokemon_number, pokemon_name, pokemon_sub_name
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pokemon_ability_partial
ON pokemon_ability (ability_name, pokemon_number, pokemon_name, pokemon_sub_name)
WHERE ability_name IS NOT NULL 
	AND pokemon_number IS NOT NULL 
	AND pokemon_name IS NOT NULL 
	AND pokemon_sub_name IS NOT NULL;
