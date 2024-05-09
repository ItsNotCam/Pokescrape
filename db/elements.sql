CREATE TABLE IF NOT EXISTS elements (
  name VARCHAR(32) PRIMARY KEY
);

CREATE INDEX IF NOT EXISTS idx_elements_name ON elements (name);