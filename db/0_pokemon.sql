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

	catch_rate_num INTEGER,
	catch_rate_percent REAL,
	friendship_num INTEGER,
	friendship_extremity VARCHAR(64),
	base_exp INTEGER,
	growth_rate VARCHAR(64),

	gender_male_percent REAL,
	gender_female_percent REAL,
	egg_cycles_num INTEGER,
	egg_cycles_steps_min INTEGER,
	egg_cycles_steps_max INTEGER,

  PRIMARY KEY (
		number, name, sub_name
	),

  -- CONSTRAINT uq_pokemon_constraint_number UNIQUE (number),
  -- CONSTRAINT uq_pokemon_constraint_name UNIQUE (name),
  -- CONSTRAINT uq_pokemon_constraint_sub_name UNIQUE (sub_name)
  CONSTRAINT uq_pokemon_constraint UNIQUE (
		number, name, sub_name
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pokemon_partial
ON pokemon (number, name, sub_name)
WHERE number IS NOT NULL 
	AND name IS NOT NULL 
	AND sub_name IS NOT NULL;