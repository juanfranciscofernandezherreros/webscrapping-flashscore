CREATE TABLE lineups (
    id BIGINT NOT NULL AUTO_INCREMENT,
    numberPlayer VARCHAR(50),
    namePlayer VARCHAR(50),
	playerId VARCHAR(50),
    starter VARCHAR(50),
	matchId VARCHAR(50),
	PRIMARY KEY (id)
);