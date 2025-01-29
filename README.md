# Smart City Surveillance

This repository implements a **real-time anomaly detection system** for camera feeds in a smart city environment. It uses **Kafka** as the message broker, **Spark Structured Streaming** for real-time inference, and a **Flask** dashboard to display anomalies.

<br/>

## Table of Contents
1. [Overview](#overview)  
2. [Core Features](#core-features)  
3. [Project Structure](#project-structure)  
4. [Setup & Installation](#setup--installation)  
5. [Usage](#usage)  
6. [Configuration](#configuration)  
7. [Troubleshooting & Tips](#troubleshooting--tips)  
8. [Future Improvements](#future-improvements)  
9. [License](#license)

<br/>

## Overview
The **Smart City Surveillance** project continuously monitors one or more video sources—local video files and/or live IP cameras—to detect anomalous events in real time. Anomalies can trigger alerts (e.g., email notifications) and are displayed on a simple web dashboard for quick review.

<br/>

## Core Features
- **Kafka Producer**: Captures frames from IP cameras or local video files, and sends them to Kafka.  
- **Spark Consumer**: Subscribes to the Kafka topic, decodes frames, and runs anomaly detection using a pre-trained neural network (autoencoder).  
- **Alert System**: Notifies stakeholders (via email, Slack, or logs) when anomalies exceed a certain threshold.  
- **Dashboard**: A Flask-based web interface to view recent anomalies and system status.  
- **Docker** & **Docker Compose**: Simplifies deployment and orchestrates services like Kafka, Zookeeper, Spark, and your app.

<br/>

## Project Structure
```
smart-city-surveillance/
├── config/
│   ├── kafka_config.json         # Kafka-related configs
│   └── alert_config.json         # Alert system configs (email, Slack, etc.)
├── data/
│   ├── testing_videos/           # Local video files for testing
│   ├── testing_vol/
│   ├── training_videos/
│   │── training_vol/
│   └── frames/
├── docker/
│   ├── Dockerfile                 # Builds your app container
│   └── entrypoint.sh              # Initialization script for the container
├── models/
│   └── anomaly_autoencoder.keras  # Trained model for anomaly detection
├── src/
│   ├── anomaly_detection/
│   │   ├── __init__.py
│   │   ├── pyspark_preprocess.py  # PySpark UDFs and preprocessing logic
│   │   ├── kafka_consumer.py      # Kafka consumer with PySpark integration
│   │   └── alert_system.py        # Alerts (email, Slack, etc.) on anomalies
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   └── kafka_producer.py      # Sends video frames to Kafka
│   ├── web_dashboard/
│   │   ├── __init__.py
│   │   ├── app.py                 # Flask web app
│   │   └── templates/
│   │       └── index.html         # Dashboard UI
├── logs/
│   └── anomalies.log              # Anomalies log file (if configured)
├── scripts/
│   ├── preprocess_video.py
│   ├── train_model.py
│   └── test_model.py
├── .dockerignore                  # Excludes unnecessary files from Docker build context
├── .gitignore                     # Prevents unnecessary files from being tracked by Git
├── docker-compose.yml             # Orchestrates Kafka, Zookeeper, Spark, App
├── requirements.txt
├── LICENSE.md                     # Licensing information for the project
└── README.md
```

<br/>

## Setup & Installation

1. **Clone this Repository**  
   ```bash
   git clone https://github.com/Kennny7/smart-city-surveillance.git
   cd smart-city-surveillance
   ```

2. **Install Docker & Docker Compose**  
   - [Docker Installation Guide](https://docs.docker.com/engine/install/)  
   - [Docker Compose](https://docs.docker.com/compose/install/)

3. **Build and Run**  
   ```bash
   docker-compose build
   docker-compose up
   ```
   This will spin up:  
   - **Zookeeper** (default port 2181)  
   - **Kafka** (default port 9092)  
   - **Spark** (default master UI at port 8080)  
   - **Flask app** (serving at port 5000)

4. **Install Python Dependencies** (optional, if running locally outside Docker)  
   ```bash
   pip install -r requirements.txt
   ```

<br/>

## Usage

### 1. Kafka Producer

- **Local**:  
  ```bash
  python src/data_ingestion/kafka_producer.py
  ```
  This reads frames from `data/testing_videos/` or your configured IP camera feeds, then publishes them to `video_topic`.

- **Inside Docker**:  
  ```bash
  docker-compose exec app python src/data_ingestion/kafka_producer.py
  ```

### 2. Kafka Consumer (Spark)
- **Local** (if Spark installed locally):  
  ```bash
  python src/anomaly_detection/kafka_consumer.py
  ```
- **Inside Docker**:
  ```bash
  docker-compose exec app python src/anomaly_detection/kafka_consumer.py
  ```

### 3. Web Dashboard
- Access the dashboard at [http://localhost:5000](http://localhost:5000)  
- Monitors anomalies (from `logs/anomalies.log` or direct pipeline)  

### 4. Alert System
- Configure your alert settings in `config/alert_config.json`  
- By default, the system can send email alerts if anomalies are detected above a threshold.

<br/>

## Configuration
- **Kafka**: Modify `config/kafka_config.json`
  ```json
  {
    "bootstrap_servers": "localhost:9092",
    "topic": "video_topic"
  }
  ```
- **Alerts**: Modify `config/alert_config.json`
  ```json
  {
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "use_tls": true,
      "sender": "example@gmail.com",
      "recipient": "recipient@gmail.com",
      "username": "example@gmail.com",
      "password": "YOUR_APP_PASSWORD"
    }
  }
  ```
- **Docker Compose**: Adjust ports, environment variables in `docker-compose.yml`  
- **Model**: By default, the `.keras` file is loaded from `models/anomaly_autoencoder.keras`. Modify `MODEL_PATH` if needed.

<br/>

## Troubleshooting & Tips
1. **Kafka Connection Issues**  
   - Ensure `kafka` container is healthy (`docker-compose logs kafka`).  
   - Check `kafka_config.json` and environment vars.

2. **Spark Not Reading Data**  
   - Verify the topic in Spark matches the one in `kafka_producer.py`.  
   - Check Spark logs via `docker-compose logs spark`.

3. **Frames Not Being Sent**  
   - Make sure your video sources in `kafka_producer.py` are correct and accessible.  
   - For IP cameras, verify your RTSP/HTTP URL is correct.

4. **High CPU/Memory Usage**  
   - Consider sampling frames (lower FPS) to reduce load.  
   - Use broadcast variables or `mapPartitions` for model loading in Spark.

<br/>

## Future Improvements
- **Scaling Up**: Multiple Spark workers, load balancing multiple camera feeds.  
- **Advanced Alerting**: Slack notifications, integration with city monitoring system.  
- **Preprocessing Optimization**: Offload heavy transforms to GPU or use more efficient codecs.  
- **Kubernetes Deployment**: For production-grade scaling, consider Helm charts and container orchestration.

<br/>

## License
This project is distributed under the [MIT License](LICENSE).

---

**Happy Monitoring!**  
Feel free to [open an issue](https://github.com/Kennny7/smart-city-surveillance/issues) or contribute new features.