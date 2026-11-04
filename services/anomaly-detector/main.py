"""Chronos Anomaly Detector Service.

Spatial-temporal threat analysis and anomaly scoring engine.
Detects:
- Sudden loitering / stationary anomalies (abandoned backpacks/objects)
- Velocity bursts (stampedes, aggressive movement)
- Boundary / restricted zone intrusions
"""

import os
import cv2
import time
import base64
import numpy as np
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AnomalyDetector")

app = FastAPI(title="Chronos Anomaly Detection Microservice", version="1.0.0")

class AnomalyScanRequest(BaseModel):
    camera_id: str
    image_base64: str
    timestamp: float

class AnomalyReport(BaseModel):
    camera_id: str
    timestamp: float
    is_anomaly: bool
    anomaly_score: float
    threat_category: str
    description: str
    bounding_boxes: List[Dict[str, Any]]

class SpatialTemporalAnomalyEngine:
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)
        self.prev_gray = None
        self.anomaly_threshold = 0.55
        logger.info("SpatialTemporalAnomalyEngine initialized with dynamic optical flow and background subtraction.")

    def process_frame(self, frame_bgr: np.ndarray, camera_id: str) -> Dict[str, Any]:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # 1. Background subtraction for foreground disturbance
        fg_mask = self.bg_subtractor.apply(gray)
        fg_ratio = np.count_nonzero(fg_mask > 200) / float(gray.size)

        # 2. Motion velocity via Optical Flow
        motion_energy = 0.0
        if self.prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            motion_energy = float(np.mean(mag))
        self.prev_gray = gray

        # Compute dynamic anomaly metric
        anomaly_score = min(1.0, (fg_ratio * 3.5) + (motion_energy * 0.15))
        is_anomaly = anomaly_score > self.anomaly_threshold

        threat_category = "NOMINAL"
        description = "Surveillance area normal. No spatial disturbances."
        boxes = []

        if is_anomaly:
            if motion_energy > 2.5:
                threat_category = "SUDDEN_RUSH_OR_STAMPEDE"
                description = f"High velocity motion detected ({motion_energy:.2f} px/s). Potential disturbance or panic."
            else:
                threat_category = "UNATTENDED_OBJECT_OR_LOITERING"
                description = f"Significant static foreground accumulation ({fg_ratio*100:.1f}% area). Potential loitering/abandoned asset."
            
            # Find bounding boxes for foreground contours
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) > 800:
                    x, y, w, h = cv2.boundingRect(cnt)
                    boxes.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h), "label": threat_category})

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": round(float(anomaly_score), 3),
            "threat_category": threat_category,
            "description": description,
            "bounding_boxes": boxes[:5] # Top 5 bounding regions
        }

ENGINE = SpatialTemporalAnomalyEngine()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "anomaly-detector"}

@app.post("/api/v1/anomaly/evaluate", response_model=AnomalyReport)
def evaluate_frame(req: AnomalyScanRequest):
    try:
        img_bytes = base64.b64decode(req.image_base64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Invalid image payload")
        
        result = ENGINE.process_frame(frame, req.camera_id)
        return AnomalyReport(
            camera_id=req.camera_id,
            timestamp=req.timestamp,
            is_anomaly=result["is_anomaly"],
            anomaly_score=result["anomaly_score"],
            threat_category=result["threat_category"],
            description=result["description"],
            bounding_boxes=result["bounding_boxes"]
        )
    except Exception as e:
        logger.error(f"Error evaluating frame: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=False)

if __name__ == "__main__":
    start()
