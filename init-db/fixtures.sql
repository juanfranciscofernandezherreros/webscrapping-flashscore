CREATE TABLE fixtures (
    id BIGINT NOT NULL AUTO_INCREMENT,
    matchId VARCHAR(200),
    fecha VARCHAR(200),
	homeTeamLogo VARCHAR(200),
	visitorTeamLogo VARCHAR(200),
	homeTeam VARCHAR(200),
	visitorTeam VARCHAR(200),
	country VARCHAR(200),
	competition VARCHAR(200),
	PRIMARY KEY (id)
);