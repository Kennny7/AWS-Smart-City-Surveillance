# Agentic Threat Ontology - Architecture & Graph Guide

<details>
<summary><b>🔍 Directory Structure (Click to expand)</b></summary>

```
services/agentic-ontology/
├── docs/
│   └── guide.md
├── main.py
├── pyproject.toml
└── README.md
```
</details>

<details>
<summary><b>📐 Multi-Agent Reasoning Loop (Click to expand)</b></summary>

```mermaid
sequenceDiagram
    participant Anomaly as Anomaly Detector
    participant Recon as Biometric Recon
    participant Agent as Agentic Ontology
    participant LLM as Local Gemma-4 (10.210.8.63:8080)
    participant UI as Mission Control HUD

    Anomaly->>Agent: Spatial Disturbance Alert
    Recon->>Agent: Subject Biometric Match
    Agent->>Agent: Update In-Memory Directed Graph
    Agent->>LLM: Prompt with Context & Graph Relations
    LLM-->>Agent: Synthesize Tactical Threat Summary & Directive
    Agent->>UI: Stream Live Threat Narrative & Action Plan
```
</details>
