# src/data_ingestion/kafka_producer.py

import json
import time
import cv2
import base64
from kafka import KafkaProducer


# =======================
# 1. LOAD KAFKA CONFIG
# =======================
def load_kafka_config(config_path='config/kafka_config.json'):
    with open(config_path) as f:
        config = json.load(f)
    return config


# =======================
# 2. CREATE PRODUCER
# =======================
def create_kafka_producer(bootstrap_servers):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    return producer


# =======================
# 3. PUBLISH FRAMES
# =======================
def publish_frames(producer, topic, source, fps_limit=None):
    cap = cv2.VideoCapture(source)
    if fps_limit:
        frame_interval = 1.0 / fps_limit
        last_frame_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if fps_limit:
            now = time.time()
            if (now - last_frame_time) < frame_interval:
                continue
            last_frame_time = now
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        producer.send(topic, value=frame_b64.encode('utf-8'))
    cap.release()


# =======================
# 4. MAIN FUNCTION
# =======================
def main():
    config = load_kafka_config()
    bootstrap_servers = config.get("bootstrap_servers", "localhost:9092")
    topic = config.get("topic", "video_topic")
    producer = create_kafka_producer(bootstrap_servers)

    # Local or network sources
    local_video_paths = [
        "data/testing_videos/test1.mp4",
        "data/testing_videos/test2.mp4"
    ]
    ip_camera_feeds = [
        # "rtsp://username:password@192.168.0.101:554/Streaming/Channels/1",
        # "http://192.168.0.102:8080/video"
    ]

    # =======================
    # 5. LOOP OVER SOURCES
    # =======================
    for source in local_video_paths + ip_camera_feeds:
        print(f"Publishing from source: {source}")
        publish_frames(producer, topic, source, fps_limit=5)

    # =======================
    # 6. FLUSH AND CLOSE
    # =======================
    producer.flush()
    producer.close()


if __name__ == "__main__":
    main()
