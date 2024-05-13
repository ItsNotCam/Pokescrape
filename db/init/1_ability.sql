CREATE TABLE IF NOT EXISTS ability (
	name VARCHAR(64) PRIMARY KEY,
	description TEXT NOT NULL,
	generation INTEGER NOT NULL
);
CREATE INDEX idx_ability_name ON ability (name);
