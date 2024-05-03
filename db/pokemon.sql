CREATE TABLE IF NOT EXISTS pokemon (
  number INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL,
  sub_name VARCHAR(255),
  icon_path VARCHAR(255) NOT NULL DEFAULT 'icons/default.png',
  total INTEGER NOT NULL,
  hp INTEGER NOT NULL,
  attack INTEGER NOT NULL,
  defense INTEGER NOT NULL,
  special_attack INTEGER NOT NULL,
  special_defense INTEGER NOT NULL,
  speed INTEGER NOT NULL,

  PRIMARY KEY (number, name, sub_name)
)