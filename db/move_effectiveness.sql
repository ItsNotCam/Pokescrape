CREATE TABLE IF NOT EXISTS move_effectiveness (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	dmg_source VARCHAR(64) NOT NULL,
	dmg_dest VARCHAR(64) NOT NULL,
	effectiveness VARCHAR(64) NOT NULL,

	FOREIGN KEY (dmg_source) REFERENCES elements(name),
	FOREIGN KEY (dmg_dest) REFERENCES elements(name)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_dmg_source ON move_effectiveness (dmg_source);
CREATE INDEX IF NOT EXISTS idx_dmg_dest ON move_effectiveness (dmg_dest);
CREATE INDEX IF NOT EXISTS idx_effectiveness ON move_effectiveness (effectiveness);