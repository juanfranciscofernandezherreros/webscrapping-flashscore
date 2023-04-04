CREATE TABLE archive (
    id BIGINT NOT NULL AUTO_INCREMENT,
    country VARCHAR(50),
    league VARCHAR(50),
	sessionYear VARCHAR(50),
    teamName VARCHAR(50),
	teamId VARCHAR(50),
	PRIMARY KEY (id)
);