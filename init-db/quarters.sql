CREATE TABLE quarters (
    id BIGINT NOT NULL AUTO_INCREMENT,
    attribute VARCHAR(50),
    homePercentage VARCHAR(50),
	visitorPercentage VARCHAR(50),
	matchId VARCHAR(50),
	PRIMARY KEY (id)
);