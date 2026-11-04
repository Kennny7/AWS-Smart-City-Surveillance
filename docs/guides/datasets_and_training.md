# Training Datasets & 3D Profiling Integration Guide

This guide explains how to acquire public surveillance datasets, ingest custom video footage, and build 3D facial profiles for the Chronos biometric database.

---

## 1. Recommended Open-Source Datasets

You can download and extract these datasets directly to run training or offline evaluations:

| Dataset | Focus | Download Reference / Source |
| :--- | :--- | :--- |
| **UCSD Anomaly Detection Dataset** | Pedestrian walkways, bike intrusions, loitering | [UCSD Vision Lab](http://www.svcl.ucsd.edu/projects/anomaly/dataset.htm) |
| **Avenue Dataset** | Abnormal human actions in public areas | [CUHK Avenue Dataset](http://www.ee.cuhk.edu.hk/~ccloy/project_cuavenue/) |
| **ShanghaiTech Campus Dataset** | Large-scale complex city surveillance video | [ShanghaiTech Vision](https://svip-lab.github.io/dataset/campus_dataset.html) |
| **Labeled Faces in the Wild (LFW)** | Biometric verification & facial matching | [LFW Dataset](http://vis-www.cs.umass.edu/lfw/) |
| **CelebA** | High-variance face recognition & landmarks | [CelebA Dataset](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) |

---

## 2. Creating & Verifying 3D Face Profiles

1. **Capture Facial Frames**:
 Place face images into `data/sample_faces/` (e.g. `subject_01.jpg`).
2. **Execute 3D Morphometry Extraction**:
 The `biometric-recon` microservice automatically computes 468 Cartesian landmarks $(X, Y, Z)$ and outputs standard Wavefront `.OBJ` mesh files to:
 `data/3d_profiles/<SUBJECT_ID>.obj`
3. **Inspect in 3D**:
 The generated `.OBJ` files can be visualized directly inside the **Mission Control HUD** or opened in any 3D tool (Blender, MeshLab, Three.js).
4. **Human-in-the-Loop Verification**:
 Unverified profiles are queued in the HITL terminal for operator sign-off before being granted verified clearance.
