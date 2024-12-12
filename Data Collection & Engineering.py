from kafka import KafkaProducer
import boto3
import json
import time
from aws_kinesisagg import KinesisAggregator

# Kafka Producer setup for local processing
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# AWS Kinesis setup for cloud streaming
kinesis = boto3.client('kinesis')
agg = KinesisAggregator()

while True:
    sensor_data = {
        'bin_id': 'BIN001',
        'weight': 45.6,
        'waste_type': 'plastic',
        'temperature': 23.5,
        'humidity': 60,
        'timestamp': time.time()
    }
    
    # Send data to Kafka for local processing
    producer.send('waste_data', json.dumps(sensor_data).encode('utf-8'))
    
    # Send aggregated data to Kinesis for cloud processing
    agg.add_user_record('waste_stream', json.dumps(sensor_data).encode('utf-8'))
    if agg.has_records():
        records = agg.flush_records()
        for record in records:
            kinesis.put_record(
                StreamName='WasteManagementStream',
                Data=record,
                PartitionKey='partitionkey'
            )
    time.sleep(10)
