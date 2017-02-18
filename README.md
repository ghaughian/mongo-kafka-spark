# mongo-kafka #

A Kafka Producer extracts data from raw json file then transforms and publishes it downstream to a Kafka Consumer that performs aggregations on small batches of data before inserting the results into MongoDB.

## To Run ##

##### start zookeeper #####

`$KAFKA_HOME/bin/zookeeper-server-start.sh config/zookeeper.properties`

##### start kafka server #####

`$KAFKA_HOME/bin/kafka-server-start.sh config/server.properties`

##### create kafka topic #####

`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2182 --replication-factor 1 --partitions 1 --topic mytopic`

##### start mongod instance #####

`$MONGODB_HOME/bin/mongod` 

##### start producer #####

`python etl_producer.py`

##### start consumer #####

`python analytics_consumer_mongo.py localhost 27017 kafka`

## Python Dependencies ##
- confluent_kafka
- pymongo
- pandas
- json
