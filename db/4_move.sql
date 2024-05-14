CREATE TABLE IF NOT EXISTS move (
  name VARCHAR(255) UNIQUE PRIMARY KEY,
  element_name VARCHAR(255) NOT NULL,
  dmg_category VARCHAR(32),
  power INTEGER,
  accuracy INTEGER,
  pp INTEGER,
  description TEXT NOT NULL,
  probability INTEGER,
	
  FOREIGN KEY (element_name) REFERENCES element(name),

	CONSTRAINT uq_move_constraint UNIQUE (name)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_move_partial
ON move (name, element_name)
WHERE name IS NOT NULL 
	AND element_name IS NOT NULL;