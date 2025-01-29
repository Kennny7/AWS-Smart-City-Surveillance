### File: src/anomaly_detection/kafka_consumer.py
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.anomaly_detection.pyspark_preprocess import infer_udf, handle_anomalies_in_batch

# =======================
# 1. LOAD KAFKA CONFIG
# =======================
def load_kafka_config(config_path='config/kafka_config.json'):
    with open(config_path) as f:
        config = json.load(f)
    return config

# =======================
# 2. CREATE SPARK SESSION
# =======================
def create_spark_session():
    spark = (SparkSession.builder
             .appName("RealTimeAnomalyDetection")
             .getOrCreate())
    return spark

# =======================
# 3. MAIN STREAMING LOGIC
# =======================
def main():
    # Load Kafka configurations
    config = load_kafka_config()
    bootstrap_servers = config.get("bootstrap_servers", "localhost:9092")
    topic = config.get("topic", "video_topic")

    # Create a Spark session
    spark = create_spark_session()

    # Read Kafka stream
    df = (spark.readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", bootstrap_servers)
          .option("subscribe", topic)
          .load())

    # Extract and preprocess Kafka data
    raw_df = df.selectExpr("CAST(value AS STRING) AS raw_frame_b64")
    results_df = raw_df.withColumn("anomaly_result", infer_udf(col("raw_frame_b64")))

    # Use foreachBatch to process anomalies and send alerts
    query = (results_df.writeStream
             .outputMode("append")
             .foreachBatch(handle_anomalies_in_batch)
             .start())

    query.awaitTermination()

if __name__ == "__main__":
    main()


