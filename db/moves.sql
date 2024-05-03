CREATE TABLE IF NOT EXISTS moves (
  name VARCHAR(255) PRIMARY KEY,
  element_name VARCHAR(255) NOT NULL,
  dmg_category VARCHAR(32),
  power INTEGER NOT NULL,
  accuracy INTEGER NOT NULL,
  pp INTEGER NOT NULL,
  description TEXT NOT NULL,
  probability INTEGER NOT NULL,
  FOREIGN KEY (element_name) REFERENCES elements(name)
)