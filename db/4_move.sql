CREATE TABLE IF NOT EXISTS move (
  name VARCHAR(255) PRIMARY KEY,
  element_name VARCHAR(255) NOT NULL,
  dmg_category VARCHAR(32),
  power INTEGER,
  accuracy INTEGER,
  pp INTEGER,
  description TEXT NOT NULL,
  probability INTEGER,
	
  FOREIGN KEY (element_name) REFERENCES element(name)
);

CREATE INDEX idx_move_name ON move (name);
CREATE INDEX idx_move_element_name ON move (element_name);