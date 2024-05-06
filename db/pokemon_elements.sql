CREATE TABLE IF NOT EXISTS pokemon_elements (
  pokemon_number INTEGER,
  pokemon_name VARCHAR(255),
  pokemon_sub_name VARCHAR(255),
  element_name VARCHAR(255),
  
  FOREIGN KEY (pokemon_number) REFERENCES pokemon(number),
  FOREIGN KEY (pokemon_name) REFERENCES pokemon(name),
  FOREIGN KEY (pokemon_sub_name) REFERENCES pokemon(sub_name),
  FOREIGN KEY (element_name) REFERENCES elements(name),

  PRIMARY KEY (pokemon_number, pokemon_name, pokemon_sub_name, element_name)
)