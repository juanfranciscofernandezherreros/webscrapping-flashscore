CREATE TABLE pointByPoints (
    id BIGINT NOT NULL AUTO_INCREMENT,
    actionLocal VARCHAR(200),
	totalPointsLocal VARCHAR(200),
	totalPointsVisitor VARCHAR(200),	
	actionVisitor VARCHAR(200),
	quarter VARCHAR(200),
	matchId VARCHAR(200),
    PRIMARY KEY (id)
);