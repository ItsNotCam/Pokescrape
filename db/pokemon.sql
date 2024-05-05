CREATE TABLE IF NOT EXISTS pokemon (
  number INTEGER NOT NULL,
  name VARCHAR(64) NOT NULL,
  sub_name VARCHAR(64),
  icon_path VARCHAR(64) NOT NULL DEFAULT 'icons/default.png',
  total INTEGER NOT NULL,
  hp INTEGER NOT NULL,
  attack INTEGER NOT NULL,
  defense INTEGER NOT NULL,
  special_attack INTEGER NOT NULL,
  special_defense INTEGER NOT NULL,
  speed INTEGER NOT NULL,

	species VARCHAR(64) NOT NULL,
	height REAL NOT NULL,
	weight REAL NOT NULL,

	-- ev_amount INTEGER NOT NULL,
	-- ev_type VARCHAR(64) NOT NULL,
	catch_rate_num INTEGER NOT NULL,
	catch_rate_percent REAL NOT NULL,
	friendship_num INTEGER NOT NULL,
	friendship_extremity VARCHAR(64) NOT NULL,
	base_exp INTEGER NOT NULL,
	growth_rate VARCHAR(64) NOT NULL,

	gender_male_percent REAL NOT NULL,
	gender_female_percent REAL NOT NULL,
	egg_cycles_num INTEGER NOT NULL,
	egg_cycles_steps_min INTEGER NOT NULL,
	egg_cycles_steps_max INTEGER NOT NULL,

  PRIMARY KEY (number, name, sub_name)
)