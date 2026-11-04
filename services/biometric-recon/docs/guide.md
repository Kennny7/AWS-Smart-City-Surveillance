# Biometric Reconnaissance - Engineering & 3D Guide

<details>
<summary><b> Directory Structure (Click to expand)</b></summary>

```
services/biometric-recon/
 docs/
 guide.md
 main.py
 pyproject.toml
 README.md
```
</details>

<details>
<summary><b> 3D Biometric Morphometry & HITL Pipeline (Click to expand)</b></summary>

```mermaid
sequenceDiagram
 participant UI as Mission Control HUD
 participant Recon as Biometric Recon Engine
 participant Mesh as 3D OBJ Generator
 participant Storage as MinIO/Local Disk
 participant HITL as Human-in-the-Loop Operator

 UI->>Recon: Post Target Frame
 Recon->>Recon: Detect Faces & 468 3D Landmarks
 Recon->>Mesh: Compute (X, Y, Z) Cartesian coordinates
 Mesh->>Storage: Persist .OBJ Wavefront Model
 Recon->>HITL: Enqueue Identity for Manual Operator Review
 HITL->>Recon: Approve / Reject Clearance
```
</details>
