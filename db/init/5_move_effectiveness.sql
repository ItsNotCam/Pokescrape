CREATE TABLE IF NOT EXISTS move_effectiveness (
	id INTEGER  AUTO_INCREMENT PRIMARY KEY,
	dmg_source VARCHAR(64) NOT NULL,
	dmg_dest VARCHAR(64) NOT NULL,
	effectiveness INT NOT NULL,

	FOREIGN KEY (dmg_source) REFERENCES element(name),
	FOREIGN KEY (dmg_dest) REFERENCES element(name)
);

CREATE INDEX idx_move_dmg_source ON move_effectiveness (dmg_source);
CREATE INDEX idx_move_dmg_dest ON move_effectiveness (dmg_dest);
CREATE INDEX idx_move_effectiveness ON move_effectiveness (effectiveness);