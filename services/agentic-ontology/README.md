# Chronos Surveillance OS - Agentic Threat Ontology

Autonomous threat reasoning and multi-agent knowledge graph engine connected to your local Gemma-4 LLM server.

---

## 📌 Architecture & Ontology Relations

```mermaid
graph TD
    A[Camera Feed Node] -->|MONITORS| B[City Sector]
    A -->|OBSERVED_SUBJECT| C[Citizen / Person of Interest]
    C -->|INVOLVED_IN| D[Threat / Anomaly Event]
    D -->|EVALUATED_BY| E[Gemma-4 Local LLM Agent]
    E -->|ISSUES_DIRECTIVE| F[Tactical Dispatch / HITL Action]
```

---

## 🚀 Quickstart Guide

### For Newbies
1. `cd services/agentic-ontology`
2. `uv sync`
3. `uv run python main.py`
4. Inspect graph schema at `http://localhost:8003/docs`
