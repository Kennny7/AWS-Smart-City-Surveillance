# Chronos Mission Control UI

Cyber-tactical surveillance and 3D intelligence dashboard built for city-scale command centers.

---

## 📌 Features & Visual HUD

- **Cyber-Tactical HUD**: Dark-mode target acquisition reticles, biometric bounding cards, and live telemetry overlays matching defense-grade surveillance operations.
- **Biometric Identity Card**: Clean, non-null intelligence profiles displaying confirmed OSINT identities, security clearance, confidence scores, and professional stats.
- **3D Facial Morphometry Visualizer**: Inspects 468-point 3D landmark point clouds and exports Wavefront `.OBJ` meshes.
- **Human-in-the-Loop (HITL) Queue**: Real-time review and clearance interface for field operators to approve or flag tracked individuals.
- **Agentic Threat Narrative Terminal**: Integrates with local Gemma-4 LLM to output real-time tactical directives and knowledge-graph associations.

---

## 🚀 Quickstart Guide

### For Newbies
1. `cd services/mission-control-ui`
2. `uv sync`
3. `uv run streamlit run app.py`
4. Access the UI in your web browser at: `http://localhost:8501`

### Testing with Custom Video or Phone Stream
1. In the sidebar under **Sensor & Feed Gateway**, select your camera feed source.
2. Select or register your smartphone IP stream (`http://<phone_ip>:8080/video`) or your laptop webcam (`0`).
3. View real-time biometric tracking, 3D face mesh reconstruction, and agentic reasoning.
