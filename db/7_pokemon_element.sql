CREATE TABLE IF NOT EXISTS pokemon_element (
  element_name VARCHAR(255),
	pokemon_number INTEGER,
  pokemon_name VARCHAR(255),
  pokemon_sub_name VARCHAR(255),

  CONSTRAINT fk_element_name 
	FOREIGN KEY (element_name)
	REFERENCES element(name),

	CONSTRAINT fk_pokemon_element FOREIGN KEY (
		pokemon_number, pokemon_name, pokemon_sub_name
	) REFERENCES pokemon(
		number, name, sub_name
	),

	PRIMARY KEY (
		element_name, pokemon_number, pokemon_name, pokemon_sub_name
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pokemon_element_partial
ON pokemon_element (element_name, pokemon_number, pokemon_name, pokemon_sub_name)
WHERE element_name IS NOT NULL AND pokemon_number IS NOT NULL AND pokemon_name IS NOT NULL AND pokemon_sub_name IS NOT NULL;
