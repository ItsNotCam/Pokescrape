CREATE TABLE IF NOT EXISTS ability (
	name VARCHAR(64) UNIQUE PRIMARY KEY,
	description TEXT NOT NULL,
	generation INTEGER NOT NULL,

	CONSTRAINT uq_ability_constraint UNIQUE (
		name
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_ability_name ON ability (name);
