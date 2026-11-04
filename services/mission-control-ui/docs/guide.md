# Mission Control UI - Operator & Developer Manual

<details>
<summary><b>🔍 Directory Structure (Click to expand)</b></summary>

```
services/mission-control-ui/
├── docs/
│   └── guide.md
├── app.py
├── pyproject.toml
└── README.md
```
</details>

<details>
<summary><b>📐 Frontend Component & Data Flow (Click to expand)</b></summary>

```mermaid
graph TD
    subgraph Microservices Layer
        IG[Ingestion Gateway :8001]
        AD[Anomaly Detector :8004]
        BR[Biometric Recon :8002]
        AO[Agentic Ontology :8003]
    end

    subgraph Mission Control HUD :8501
        StreamCanvas[Live Tactical Video HUD Canvas]
        BioCard[Subject Intelligence Card & Stats]
        MeshViewer[3D Facial Mesh Inspector]
        HITLPanel[HITL Verification Interface]
        AgentTerminal[Gemma-4 Directive Stream]
    end

    IG -->|MJPEG / B64 Frames| StreamCanvas
    AD -->|Threat Score & Contours| StreamCanvas
    BR -->|468 3D Landmarks & OSINT Profile| BioCard
    BR -->|.OBJ Mesh Output| MeshViewer
    BR -->|Pending Clearances| HITLPanel
    AO -->|Graph Narrative & Directive| AgentTerminal
```
</details>

## 🎮 Operator Controls
1. **Re-Scan Frame**: Triggers an instant snapshot analysis across all AI microservices.
2. **Force 3D Recon**: Generates and persists a 468-point 3D facial coordinate mesh `.OBJ` for the primary subject in view.
3. **Confirm Clearance Action**: Submits Human-in-the-Loop decision (`APPROVE_IDENTITY`, `FLAG_AS_ANOMALY`, or `REQUEST_HIGH_RES_SCAN`) and logs it in the ontology knowledge graph.
