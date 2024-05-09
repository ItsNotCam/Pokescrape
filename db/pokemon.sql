CREATE TABLE IF NOT EXISTS pokemon (
  number INTEGER NOT NULL,
  name VARCHAR(64) NOT NULL,
  sub_name VARCHAR(64),
  icon_path VARCHAR(64) NOT NULL DEFAULT 'default.png',
  total INTEGER NOT NULL,
  hp INTEGER NOT NULL,
  attack INTEGER NOT NULL,
  defense INTEGER NOT NULL,
  special_attack INTEGER NOT NULL,
  special_defense INTEGER NOT NULL,
  speed INTEGER NOT NULL,

	species VARCHAR(64) NOT NULL,
	height REAL,
	weight REAL,

	catch_rate_num INTEGER NOT NULL,
	catch_rate_percent REAL NOT NULL,
	friendship_num INTEGER,
	friendship_extremity VARCHAR(64),
	base_exp INTEGER NOT NULL,
	growth_rate VARCHAR(64) NOT NULL,

	gender_male_percent REAL,
	gender_female_percent REAL,
	egg_cycles_num INTEGER,
	egg_cycles_steps_min INTEGER,
	egg_cycles_steps_max INTEGER,

  PRIMARY KEY (name, sub_name)
);

CREATE INDEX IF NOT EXISTS idx_number ON pokemon (number);
CREATE INDEX IF NOT EXISTS idx_pokemon_name ON pokemon (name);
CREATE INDEX IF NOT EXISTS idx_pokemon_sub_name ON pokemon (sub_name);
CREATE INDEX IF NOT EXISTS idx_species ON pokemon (species);