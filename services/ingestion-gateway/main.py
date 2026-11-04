"""Chronos Surveillance OS - Ingestion Gateway.

Universal multi-camera video ingestion supporting:
- RTSP / ONVIF IP surveillance feeds
- Smartphone IP cameras (e.g. DroidCam, IP Webcam HTTP/MJPEG)
- Laptop integrated / USB webcams
- Local MP4 / AVI test recordings in continuous loop
- REST API for dynamic camera registration and live health heartbeats
"""

import os
import cv2
import time
import json
import base64
import logging
import threading
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IngestionGateway")

app = FastAPI(
    title="Chronos Ingestion Gateway",
    version="1.0.0",
    description="Universal RTSP, Mobile, USB & IP Surveillance Gateway for Chronos OS"
)

# Active streams registry: {camera_id: VideoCaptureManager}
ACTIVE_STREAMS: Dict[str, "CameraStreamManager"] = {}

class CameraRegistration(BaseModel):
    camera_id: str
    source_url: str  # Can be "0" for webcam, "rtsp://...", "http://...", or file path
    location: str = "Metropolis Sector Alpha"
    camera_type: str = "RTSP_FIXED"  # CCTV, MOBILE_PHONE, LAPTOP_CAM, DRONE
    fps_limit: int = 15

class CameraStreamManager:
    def __init__(self, config: CameraRegistration):
        self.config = config
        self.camera_id = config.camera_id
        self.source = int(config.source_url) if config.source_url.isdigit() else config.source_url
        self.cap: Optional[cv2.VideoCapture] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.last_frame: Optional[bytes] = None
        self.last_frame_b64: Optional[str] = None
        self.frame_count = 0
        self.status = "INITIALIZING"

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        logger.info(f"Stream capture initialized for [{self.camera_id}] from source '{self.source}'")

    def _capture_loop(self):
        try:
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                self.status = "OFFLINE"
                logger.warning(f"Could not open camera stream {self.source}. Simulating synthetic surveillance feed.")
                self._synthetic_loop()
                return

            self.status = "STREAMING"
            frame_interval = 1.0 / max(1, self.config.fps_limit)

            while self.running:
                t_start = time.time()
                ret, frame = self.cap.read()
                if not ret:
                    if isinstance(self.source, str) and os.path.exists(self.source):
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    time.sleep(0.5)
                    continue

                self.frame_count += 1
                frame = cv2.resize(frame, (640, 360))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_bytes = buffer.tobytes()
                self.last_frame = frame_bytes
                self.last_frame_b64 = base64.b64encode(frame_bytes).decode('utf-8')

                elapsed = time.time() - t_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except Exception as e:
            self.status = "ERROR"
            logger.error(f"Error on stream {self.camera_id}: {e}")
            self._synthetic_loop()
        finally:
            if self.cap:
                self.cap.release()

    def _synthetic_loop(self):
        """Simulate high-tech tactical CCTV frame if physical hardware is offline."""
        import numpy as np
        self.status = "SYNTHETIC_SIMULATION"
        logger.info(f"Running synthetic surveillance simulation for {self.camera_id}")
        
        while self.running:
            img = np.zeros((360, 640, 3), dtype=np.uint8)
            for x in range(0, 640, 40):
                cv2.line(img, (x, 0), (x, 360), (20, 28, 20), 1)
            for y in range(0, 360, 40):
                cv2.line(img, (0, y), (640, y), (20, 28, 20), 1)
                
            t_now = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(img, f"CHRONOS CITY GRID FEED - {self.camera_id}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
            cv2.putText(img, f"LOC: {self.config.location} | TIME: {t_now}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
            cv2.putText(img, "[SYSTEM ACTIVE: RECON SCANNER ENGAGED]", (20, 340),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)
            
            x_box = int(250 + 100 * np.sin(time.time()))
            y_box = int(120 + 30 * np.cos(time.time()))
            cv2.rectangle(img, (x_box, y_box), (x_box + 120, y_box + 140), (0, 255, 0), 2)
            cv2.putText(img, "SUBJECT-ALPHA", (x_box, y_box - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            _, buffer = cv2.imencode('.jpg', img)
            self.last_frame = buffer.tobytes()
            self.last_frame_b64 = base64.b64encode(self.last_frame).decode('utf-8')
            self.frame_count += 1
            time.sleep(1.0 / self.config.fps_limit)

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        self.status = "STOPPED"

@app.on_event("startup")
def startup_event():
    logger.info("Initializing Chronos Ingestion Gateway...")
    primary_src = os.getenv("PRIMARY_CAMERA_SOURCE", "0")
    reg = CameraRegistration(
        camera_id="CAM_NODE_01",
        source_url=primary_src,
        location="Metropolis Central Plaza",
        camera_type="PRIMARY_FEED",
        fps_limit=15
    )
    manager = CameraStreamManager(reg)
    manager.start()
    ACTIVE_STREAMS[reg.camera_id] = manager

@app.on_event("shutdown")
def shutdown_event():
    for manager in ACTIVE_STREAMS.values():
        manager.stop()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ingestion-gateway",
        "active_cameras": len(ACTIVE_STREAMS),
        "streams": {cid: m.status for cid, m in ACTIVE_STREAMS.items()}
    }

@app.post("/api/v1/cameras/register")
def register_camera(config: CameraRegistration):
    if config.camera_id in ACTIVE_STREAMS:
        ACTIVE_STREAMS[config.camera_id].stop()
    
    manager = CameraStreamManager(config)
    manager.start()
    ACTIVE_STREAMS[config.camera_id] = manager
    return {"message": f"Camera {config.camera_id} registered and ingestion started.", "config": config}

@app.get("/api/v1/cameras")
def list_cameras():
    results = []
    for cid, m in ACTIVE_STREAMS.items():
        results.append({
            "camera_id": cid,
            "location": m.config.location,
            "type": m.config.camera_type,
            "status": m.status,
            "frames_processed": m.frame_count
        })
    return {"cameras": results}

@app.get("/api/v1/cameras/{camera_id}/frame")
def get_latest_frame(camera_id: str):
    if camera_id not in ACTIVE_STREAMS:
        raise HTTPException(status_code=404, detail="Camera ID not found")
    
    manager = ACTIVE_STREAMS[camera_id]
    if not manager.last_frame:
        raise HTTPException(status_code=503, detail="Frame not ready yet")
        
    return JSONResponse(content={
        "camera_id": camera_id,
        "timestamp": time.time(),
        "frame_count": manager.frame_count,
        "image_base64": manager.last_frame_b64
    })

@app.get("/api/v1/cameras/{camera_id}/mjpeg")
def mjpeg_stream(camera_id: str):
    if camera_id not in ACTIVE_STREAMS:
        raise HTTPException(status_code=404, detail="Camera ID not found")
        
    manager = ACTIVE_STREAMS[camera_id]
    
    def frame_generator():
        while manager.running:
            if manager.last_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + manager.last_frame + b'\r\n')
            time.sleep(0.06)
            
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

def start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)

if __name__ == "__main__":
    start()
