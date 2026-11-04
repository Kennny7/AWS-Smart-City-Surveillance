# Chronos Surveillance OS - Biometric Reconnaissance

3D facial morphometry reconstruction, vector-based identity matching, and Human-in-the-Loop (HITL) clearance system.

---

## 📌 Architecture & 3D Profiling Workflow

```mermaid
graph TD
    A[Video Stream Frame] --> B[MediaPipe 468-point 3D Face Mesh]
    B --> C[3D Point Cloud / Mesh Exporter .OBJ]
    C --> D[MinIO Object Storage / Local Profiles]
    B --> E[512D Vector Embedding Extraction]
    E --> F[Vector DB: Qdrant / ChromaDB]
    F --> G[OSINT & Civil Identity Registry Lookup]
    G --> H{Confidence > 0.95?}
    H -->|Yes| I[Verified Identity Stream]
    H -->|No| J[Human-In-The-Loop Review Queue]
```

---

## 🚀 Quickstart Guide

### For Newbies
1. `cd services/biometric-recon`
2. `uv sync`
3. `uv run python main.py`
4. Access docs at `http://localhost:8002/docs`
