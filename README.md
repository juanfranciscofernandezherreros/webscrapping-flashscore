https://medium.com/nagoya-foundation/simple-cdc-with-debezium-kafka-a27b28d8c3b8

kafka-topics --bootstrap-server=localhost:29092 --list
kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver1.inventory.customers --from-beginning
