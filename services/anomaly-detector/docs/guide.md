# Anomaly Detector - Developer & Operations Guide

<details>
<summary><b> Directory Structure (Click to expand)</b></summary>

```
services/anomaly-detector/
 docs/
 guide.md
 main.py
 pyproject.toml
 README.md
```
</details>

<details>
<summary><b> Algorithmic Scoring Flow (Click to expand)</b></summary>

```mermaid
flowchart TD
 Frame[Incoming Video Frame] --> Diff[Differential Gaussian Filter]
 Diff --> FG[Foreground Density Mask]
 Diff --> Flow[Dense Optical Flow Vector Field]
 FG -->|Static Area Ratio| ScoreEngine[Anomaly Threshold Evaluator]
 Flow -->|Kinetic Energy Mean| ScoreEngine
 ScoreEngine --> Decision{Threshold > 0.55?}
 Decision -->|Yes| Alert[Publish Anomaly Report to Kafka & Agent Engine]
 Decision -->|No| Nominal[Record Nominal Heartbeat]
```
</details>
