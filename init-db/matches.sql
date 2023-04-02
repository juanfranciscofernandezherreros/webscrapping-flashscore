CREATE TABLE matchs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    EventTimeUTC INT,
    EventTime VARCHAR(20),
    HomeTeam VARCHAR(50),
    AwayTeam VARCHAR(50),
    Quarter1Home VARCHAR(4),
    Quarter2Home VARCHAR(50),
    Quarter3Home VARCHAR(50),
    Quarter4Home VARCHAR(50),
    OvertimeHome VARCHAR(50),
    Quarter1Away VARCHAR(50),
    Quarter2Away VARCHAR(50),
    Quarter3Away VARCHAR(50),
    Quarter4Away VARCHAR(50),
    OvertimeAway VARCHAR(50),
	matchId VARCHAR(50),
    PRIMARY KEY (id)
);
