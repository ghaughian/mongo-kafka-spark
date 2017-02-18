import json
import pymongo
import pandas as pd
import sys
from   confluent_kafka import Consumer, KafkaError
from   pymongo import MongoClient


# extract command line args: host, port and database
usage = "python analytics_consumer_mongo.py <MongoDB_Host> <MongoDB_Port> <MongoDB_Database>"

if len(sys.argv) < 4:
    print "ERROR: Insufficient command line arguments supplied"
    print "       usage: '" + usage + "'"
    sys.exit(2)

host  = sys.argv[1]
port  = int(sys.argv[2])
database = sys.argv[3]

client = MongoClient(host, port)
db = client[database]
coll = db.agg_test

c = Consumer({'bootstrap.servers': 'localhost', 
              'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'smallest'}})
c.subscribe(['topic_json'])

def agg():
    msgs = []
    i=0
    # aggregate 10 messages at a time
    while (i<10):
        msg = c.poll()
        if not msg.error():
            print('Received message: %s' % msg.value().decode('utf-8'))
            json_msg = json.loads(msg.value())
            msgs.append(json_msg)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
        if i==9:
            df = pd.DataFrame(msgs) 
            # very basic aggregation
            aggDF = df.groupby("airline_id").count()
            coll.insert_many(aggDF.to_dict('records'))
            i=0
            msgs=[]
        else:
            i=i+1
    #c.close()

def main():
    agg()

if __name__ == "__main__": main()

# TODO: Have `agg` operate on a timer rather than x number of records e.g:
# import threading
# threading.Timer(1, ts).start()
