'''    
    spark-submit \
        --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 \
        rte.py localhost:2181 test agg_test
'''
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from confluent_kafka import Producer

USAGE = "Usage: rte.py <zookeeper_host> <topic_to_consume> <tpoic_to_produce>"
TIMER = 5

producer = Producer({'bootstrap.servers': 'localhost'})

def publish(message, topic):
    records = message.collect()
    for record in records:
        producer.produce(topic, str(record))
        producer.flush()

def aggregate(stream):
    return stream.map(lambda x: x[1]) \
        .flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)

def main():
    if len(sys.argv) != 4:
        print(USAGE)
        exit(-1)

    sc = SparkContext(appName="Realtime-Analytics-Engine")
    ssc = StreamingContext(sc, TIMER)

    zookeeper, in_topic, out_topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zookeeper, "analytics-engine-consumer", {in_topic: 1})
    aggRDD = aggregate(kvs)
    aggRDD.foreachRDD(lambda rec : publish(rec, out_topic))
    
    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__": main()
