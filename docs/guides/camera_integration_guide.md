# Universal Camera Integration Guide (CCTV, Laptops, Mobile Phones)

Chronos Surveillance OS is designed to ingest feeds from standard enterprise CCTV hardware, drones, laptops, and smartphones.

---

## 1. Connecting Your Smartphone

You can transform any iPhone or Android phone into a surveillance node on your local private network.

### Option A: Using "IP Webcam" (Android)
1. Install **IP Webcam** (by Pavel Khlebovich) from Google Play.
2. Open the app, scroll to the bottom, and tap **Start Server**.
3. The app will display an IP address on your screen, e.g.:
 `http://192.168.1.55:8080`
4. Register the camera with Chronos Ingestion Gateway:
 ```bash
 curl -X POST http://localhost:8001/api/v1/cameras/register \
 -H "Content-Type: application/json" \
 -d '{
 "camera_id": "PHONE_CAMERA_01",
 "source_url": "http://192.168.1.55:8080/video",
 "location": "Mobile Patrol Unit 1",
 "camera_type": "MOBILE_PHONE",
 "fps_limit": 15
 }'
 ```

### Option B: Using DroidCam (iOS & Android)
1. Install **DroidCam** on your phone.
2. Connect to the same Wi-Fi network as your host computer.
3. Use the MJPEG video stream URL provided by DroidCam (e.g. `http://192.168.1.55:4747/video`).

---

## 2. Connecting Laptop or USB Webcams

Chronos can access onboard laptop cameras and USB capture devices directly via hardware index.

- **Primary Integrated Webcam**: `0`
- **Secondary / External USB Webcam**: `1`

To configure:
```bash
curl -X POST http://localhost:8001/api/v1/cameras/register \
 -H "Content-Type: application/json" \
 -d '{
 "camera_id": "LAPTOP_CAM_01",
 "source_url": "0",
 "location": "Field Operative Laptop",
 "camera_type": "LAPTOP_CAM",
 "fps_limit": 15
 }'
```

---

## 3. Connecting Standard RTSP / ONVIF CCTV Cameras

For traditional security cameras, provide standard RTSP credentials:
```bash
curl -X POST http://localhost:8001/api/v1/cameras/register \
 -H "Content-Type: application/json" \
 -d '{
 "camera_id": "CCTV_TRAFFIC_INTERSECTION",
 "source_url": "rtsp://admin:security123@192.168.1.200:554/Streaming/Channels/101",
 "location": "Sector 07 North Intersection",
 "camera_type": "RTSP_FIXED",
 "fps_limit": 20
 }'
```
