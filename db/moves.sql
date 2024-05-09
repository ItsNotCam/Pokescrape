CREATE TABLE IF NOT EXISTS moves (
  name VARCHAR(255) PRIMARY KEY,
  element_name VARCHAR(255) NOT NULL,
  dmg_category VARCHAR(32),
  power INTEGER,
  accuracy INTEGER,
  pp INTEGER NOT NULL,
  description TEXT NOT NULL,
  probability INTEGER,
	
  FOREIGN KEY (element_name) REFERENCES elements(name)
);

CREATE INDEX IF NOT EXISTS idx_moves_name ON moves (name);
CREATE INDEX IF NOT EXISTS idx_moves_element_name ON moves (element_name)