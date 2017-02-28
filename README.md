# mongo-kafka #

A Kafka Producer extracts json data from a file then transforms and publishes it downstream to a realtime analytics engine that aggregates the data using SparkStreaming before publishing it back onto another Kafka topic for consumption by MongoDB.

Also illustrates how to aggregate batches of realtime data before inserting the results directly into MongoDB using Python DataFrames.

## To Run ##

##### start zookeeper #####

`$KAFKA_HOME/bin/zookeeper-server-start.sh config/zookeeper.properties`

##### start kafka server #####

`$KAFKA_HOME/bin/kafka-server-start.sh config/server.properties`

##### create kafka topics #####

`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`
`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic agg_test`

##### start mongod instance #####

`$MONGODB_HOME/bin/mongod` 

##### start producer #####

`python pub.py`

##### start realtime analytics engine #####

`spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 rte.py localhost:2181 test agg_test`

##### start python aggregation consumer that publishes directly to MongoDB #####

`python sub_agg_mongo.py localhost 27017 kafka`

## Python Dependencies ##
- confluent_kafka
- pymongo
- pandas
- json
