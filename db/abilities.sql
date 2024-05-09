CREATE TABLE IF NOT EXISTS abilities (
	name VARCHAR(64) PRIMARY KEY,
	description TEXT NOT NULL,
	generation INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_abilities_name ON abilities (name);