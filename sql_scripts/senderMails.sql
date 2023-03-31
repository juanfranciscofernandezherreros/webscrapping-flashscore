CREATE TABLE sendersMail (
    id BIGINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(20),
    hasActive VARCHAR(50),    
    PRIMARY KEY (id)
);
INSERT INTO bigdataetl.sendersMail
(id,email, hasActive)
VALUES(NULL,'kfh1992@gmail.com','Y');
INSERT INTO bigdataetl.sendersMail
(id,email, hasActive)
VALUES(NULL,'jnfz92@gmail.com','Y');