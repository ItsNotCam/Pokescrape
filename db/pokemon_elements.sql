CREATE TABLE IF NOT EXISTS pokemon_elements (
  element_name VARCHAR(255),
	pokemon_number VARCHAR(64),
  pokemon_name VARCHAR(255),
  pokemon_sub_name VARCHAR(255),

  FOREIGN KEY (element_name) REFERENCES elements(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
  FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
  FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (element_name, pokemon_number, pokemon_name, pokemon_sub_name)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_element_name ON pokemon_elements (element_name);
CREATE INDEX IF NOT EXISTS idx_elements_pokemon_number ON pokemon_elements (pokemon_number);
CREATE INDEX IF NOT EXISTS idx_elements_pokemon_name ON pokemon_elements (pokemon_name);
CREATE INDEX IF NOT EXISTS idx_elements_pokemon_sub_name ON pokemon_elements (pokemon_sub_name);