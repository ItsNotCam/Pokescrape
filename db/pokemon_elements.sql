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
)