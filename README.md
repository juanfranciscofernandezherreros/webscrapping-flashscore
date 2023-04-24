https://medium.com/nagoya-foundation/simple-cdc-with-debezium-kafka-a27b28d8c3b8

kafka-topics --bootstrap-server=localhost:9092 --list

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" 127.0.0.1:8083/connectors/ --data "@register-mysql.json"

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" 127.0.0.1:8083/connectors/ --data "@register-mongo-fixtures"


FIXTURES

kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver1.inventory.fixtures --from-beginning

docker run -p 127.0.0.1:27017:27017 --name some-mongo -d mongo

INSERT INTO inventory.urls (urls, country, isOpened, whenHasOpened) VALUES('https://www.flashscore.com/basketball/', '', 'F', );
