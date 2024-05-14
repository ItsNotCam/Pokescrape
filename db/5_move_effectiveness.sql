CREATE TABLE IF NOT EXISTS move_effectiveness (
	dmg_source VARCHAR(64) NOT NULL,
	dmg_dest VARCHAR(64) NOT NULL,
	effectiveness INT NOT NULL,

	FOREIGN KEY (dmg_source) REFERENCES element(name),
	FOREIGN KEY (dmg_dest) REFERENCES element(name),

	PRIMARY KEY (
		dmg_source, dmg_dest
	),

	CONSTRAINT uq_move_effectiveness UNIQUE (
		dmg_source, dmg_dest
	)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_move_effectiveness_partial
ON move_effectiveness (dmg_source, dmg_dest)
WHERE dmg_source IS NOT NULL 
	AND dmg_dest IS NOT NULL;
