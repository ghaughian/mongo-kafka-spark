# mongo-kafka #

A Kafka Producer ETL's json data from file and publishes it downstream to a Consumer that performs aggregations on small batches of data before inserting the results into MongoDB


#### start zookeeper ####

`$KAFKA_HOME/bin/zookeeper-server-start.sh config/zookeeper.properties`

#### start kafka server ####

`$KAFKA_HOME/bin/kafka-server-start.sh config/server.properties`

#### create kafka topic ####

`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2182 --replication-factor 1 --partitions 1 --topic mytopic`

#### start producer ####
`python etl_producer.py`

#### start consumer ####

`python analytics_consumer_mongo.py <MongoDB Host> <MongoDB Port> <MongoDB Database>`
