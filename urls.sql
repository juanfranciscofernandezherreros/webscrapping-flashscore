CREATE TABLE urls (
    id BIGINT NOT NULL AUTO_INCREMENT,
    urls VARCHAR(200) UNIQUE,
	country VARCHAR(200) UNIQUE,
	isOpened VARCHAR(200),	
	whenHasOpened int,
    PRIMARY KEY (id)
);