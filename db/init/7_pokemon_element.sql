CREATE TABLE IF NOT EXISTS pokemon_element (
  element_name VARCHAR(255),
	pokemon_number INTEGER,
  pokemon_name VARCHAR(255),
  pokemon_sub_name VARCHAR(255),

  FOREIGN KEY (element_name) REFERENCES element(name),
	FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
  FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
  FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),

	PRIMARY KEY (element_name, pokemon_number, pokemon_name, pokemon_sub_name)
);

CREATE INDEX idx_element_name ON pokemon_element (element_name);
CREATE INDEX idx_elements_pokemon_number ON pokemon_element (pokemon_number);
CREATE INDEX idx_elements_pokemon_name ON pokemon_element (pokemon_name);
CREATE INDEX idx_elements_pokemon_sub_name ON pokemon_element (pokemon_sub_name);