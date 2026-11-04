# Master Architecture - Chronos Surveillance OS

A 100% open-source, vendor-agnostic distributed surveillance intelligence operating system designed for city-scale deployments.

---

## 🏛 High-Level System Architecture

<details>
<summary><b>📐 Distributed System Architecture Diagram (Click to expand)</b></summary>

```mermaid
flowchart TD
    subgraph Data Sources & Ingestion Layer
        CCTV[CCTV / ONVIF IP Cameras]
        Phone[Smartphones / IP Webcam]
        Laptop[Laptop / USB Webcams]
        Drone[Drone / Aerial RTMP Streams]
        
        CCTV & Phone & Laptop & Drone --> IG[services/ingestion-gateway :8001]
    end

    subgraph Distributed Streaming Bus
        IG -->|Publish Frame Metadata & Events| RP[(Redpanda / Apache Kafka :9092)]
    end

    subgraph Autonomous AI Microservices
        RP -->|Frames| AD[services/anomaly-detector :8004]
        RP -->|Frames| BR[services/biometric-recon :8002]
        
        AD -->|Threat Flags & Motion Metrics| AO[services/agentic-ontology :8003]
        BR -->|Identified Entities & 3D Embeddings| AO
        
        LLM[Local Gemma-4 LLM Server\nhttp://10.210.8.63:8080/v1] <-->|Reasoning Prompts| AO
    end

    subgraph Distributed Storage Engine
        BR -->|Vector Embeddings| Qdrant[(Qdrant Vector DB :6333)]
        BR -->|3D Wavefront .OBJ Files| MinIO[(MinIO Object Store :9000)]
        AO -->|Ontology Relationships| Neo4j[(Neo4j Graph Database :7687)]
    end

    subgraph Command & Operations
        IG & AD & BR & AO --> HUD[services/mission-control-ui :8501]
        HUD -->|Human-in-the-Loop Verifications| BR
    end
```
</details>

---

## 📂 Repository Microservices Matrix

| Microservice | Path | Port | Core Responsibilities |
| :--- | :--- | :--- | :--- |
| **Ingestion Gateway** | `services/ingestion-gateway` | `8001` | RTSP, RTMP, Phone, Laptop webcam ingestion, frame resizing & streaming. |
| **Anomaly Detector** | `services/anomaly-detector` | `8004` | Optical flow, MOG2 background subtraction, crowd anomaly and stampede detection. |
| **Biometric Recon** | `services/biometric-recon` | `8002` | MediaPipe 468-point 3D landmark mesh extraction, .OBJ generation, vector search, HITL queue. |
| **Agentic Ontology** | `services/agentic-ontology` | `8003` | Graph ontology (NetworkX/Neo4j), Gemma-4 local LLM reasoning and threat directives. |
| **Mission Control UI** | `services/mission-control-ui` | `8501` | Cyber-tactical HUD, live targeting reticles, 3D face mesh viewer, operator action console. |

---

## 🔒 Security & Privacy by Design
- **100% Local / Zero Cloud Dependency**: Operates entirely within your private network or on-premise hardware.
- **Human-in-the-Loop (HITL)**: Crucial identity matching actions require manual human operator confirmation before automated actions are triggered.
- **Data Integrity**: Profile enrichments never output unverified or raw `null` values; fallback indicators maintain operational clarity.
