CREATE TABLE errors_events (
    id BIGINT NOT NULL AUTO_INCREMENT,
	nameScriptPython VARCHAR(200),
	success VARCHAR(200),	
	errors VARCHAR(200),
    PRIMARY KEY (id)
);