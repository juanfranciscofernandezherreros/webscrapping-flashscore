CREATE TABLE pointByPoints (
    id BIGINT NOT NULL AUTO_INCREMENT,
    actionLocal VARCHAR(100),
    totalPointsLocal VARCHAR(100),
    totalPointsVisitor VARCHAR(100),    
    actionVisitor VARCHAR(100),
    quarter VARCHAR(100),
    matchId VARCHAR(100),
    PRIMARY KEY (id),
    UNIQUE KEY matchid_idx (matchId, actionLocal, totalPointsLocal, totalPointsVisitor, actionVisitor, quarter)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
