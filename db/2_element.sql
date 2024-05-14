CREATE TABLE IF NOT EXISTS element (
  name VARCHAR(32) UNIQUE PRIMARY KEY,
	CONSTRAINT uq_element_constraint UNIQUE (name)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_element_name ON element (
	name
);