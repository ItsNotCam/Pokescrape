CREATE TABLE IF NOT EXISTS element (
  name VARCHAR(32) PRIMARY KEY
);
CREATE INDEX idx_element_name ON element (name);