### File: src/anomaly_detection/pyspark_preprocess.py

import base64
import cv2
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from tensorflow.keras.models import load_model
from src.anomaly_detection.alert_system import process_anomaly_event

# =======================
# 1. LOAD ANOMALY MODEL
# =======================
MODEL_PATH = "models/anomaly_autoencoder.keras"
model = load_model(MODEL_PATH)

# =======================
# 2. INFERENCE UDF
# =======================
def infer_anomaly(frame_b64):
    try:
        # Decode base64 image
        frame_bytes = base64.b64decode(frame_b64)
        np_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            return "Error: Decoding returned None"

        # Preprocess image for the model
        img_resized = cv2.resize(img, (224, 224))
        img_resized = img_resized.astype('float32') / 255.0
        img_resized = np.expand_dims(img_resized, axis=0)

        # Perform inference
        reconstruction = model.predict(img_resized)
        error = np.mean(np.abs(img_resized - reconstruction))
        threshold = 0.05
        if error > threshold:
            return f"Anomaly (error={error:.4f})"
        else:
            return f"Normal (error={error:.4f})"
    except Exception as e:
        return f"Decode/Inference Error: {str(e)}"

# Register UDF
infer_udf = udf(infer_anomaly, StringType())

# =======================
# 3. ALERT INTEGRATION
# =======================
def handle_anomalies_in_batch(batch_df, batch_id):
    # Collect to driver for PoC purposes
    rows = batch_df.collect()
    for row in rows:
        # Check if it starts with 'Anomaly'
        if row.anomaly_result.startswith("Anomaly"):
            process_anomaly_event(row.anomaly_result)
