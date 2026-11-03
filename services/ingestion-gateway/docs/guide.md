# Ingestion Gateway - Comprehensive Guide

<details>
<summary><b>🔍 Directory Tree Structure (Click to expand)</b></summary>

```
services/ingestion-gateway/
├── docs/
│   └── guide.md
├── main.py
├── pyproject.toml
└── README.md
```
</details>

<details>
<summary><b>📐 Stream Pipeline Architecture (Click to expand)</b></summary>

```mermaid
sequenceDiagram
    participant Cam as Video Camera / Phone
    participant IG as Ingestion Gateway
    participant Broker as Redpanda Message Bus
    participant AI as Downstream AI Services

    Cam->>IG: Continuous RTSP / MJPEG Stream
    IG->>IG: Buffer, Normalize Resolution (640x360)
    IG->>Broker: Publish chronos.video.raw-frames
    IG->>AI: Direct MJPEG Loop for Tactical HUD
```
</details>

## 📱 Connecting Your Phone or Laptop
- **Android / iPhone**: Install **IP Webcam** or **DroidCam**, connect to your local Wi-Fi, and register the provided IP stream.
- **Laptop Webcam**: Use source index `0` or `1`.
