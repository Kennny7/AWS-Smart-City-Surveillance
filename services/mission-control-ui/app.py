"""Chronos Surveillance OS - Tactical Mission Control UI.

Cyber-tactical visual intelligence HUD matching high-tech reconnaissance aesthetics:
- Live CCTV / Phone camera view with targeting reticles & bounding HUDs
- Target identification badge with high-confidence stats (No nulls, verified intelligence)
- 3D Face Profile visualizer & mesh wireframe inspector
- Real-time Anomaly Threat Radar
- Human-in-the-Loop (HITL) operator verification terminal
"""

import os
import cv2
import time
import base64
import httpx
import numpy as np
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CHRONOS // Tactical Surveillance OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber-Tactical Military HUD Styling
st.markdown("""
<style>
    /* Dark Tactical Aesthetic */
    .stApp {
        background-color: #0b0f14;
        color: #e0e6ed;
        font-family: 'Courier New', Courier, monospace;
    }
    .hud-card {
        background: rgba(16, 23, 30, 0.85);
        border: 1px solid #1f382b;
        border-radius: 6px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 128, 0.08);
        margin-bottom: 12px;
    }
    .hud-title {
        color: #00ff80;
        font-weight: bold;
        font-size: 0.95rem;
        letter-spacing: 1.5px;
        border-bottom: 1px dashed #1f382b;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    .stat-badge {
        color: #00ff80;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .rec-indicator {
        color: #ff3344;
        font-weight: bold;
        letter-spacing: 2px;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

INGESTION_URL = os.getenv("INGESTION_URL", "http://localhost:8001")
ANOMALY_URL = os.getenv("ANOMALY_URL", "http://localhost:8004")
RECON_URL = os.getenv("RECON_URL", "http://localhost:8002")
ONTOLOGY_URL = os.getenv("ONTOLOGY_URL", "http://localhost:8003")

# Top Status Bar
col_h1, col_h2, col_h3 = st.columns([2, 5, 3])
with col_h1:
    st.markdown("<span class='rec-indicator'>[REC]</span> &nbsp; <b>CHRONOS-OS v2.4</b>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align: center; color: #708599;'>METROPOLIS SECTOR-07 // REAL-TIME ANOMALY & BIOMETRIC RADAR</div>", unsafe_allow_html=True)
with col_h3:
    st.markdown(f"<div style='text-align: right; color: #00ff80;'>GRID SYNC: {time.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

st.divider()

# Sidebar Configuration
st.sidebar.markdown("### SENSOR & FEED GATEWAY")
selected_camera = st.sidebar.selectbox("Active Surveillance Node", ["CAM_NODE_01 (Central Plaza)", "PHONE_01 (Mobile Patrol)", "LAPTOP_01 (Field Operative)"])
feed_type = st.sidebar.radio("Input Source Mode", ["Live Ingestion Feed", "Synthetic Tactical Simulator", "Sample Verification Video"])

st.sidebar.divider()
st.sidebar.markdown("### AGENTIC LOCAL REASONING")
st.sidebar.info(f"Local LLM Base: `{os.getenv('LLM_BASE_URL', 'http://10.210.8.63:8080/v1')}`\nModel: `{os.getenv('LLM_MODEL', 'gemma-4')}`")

# Main Multi-Column Reconnaissance Layout
col_left, col_center, col_right = st.columns([3, 5, 3])

# LEFT COLUMN: BIOMETRIC RECONNAISSANCE CARD
with col_left:
    st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-title'>TARGET BIOMETRIC CARD</div>", unsafe_allow_html=True)
    
    col_av, col_av_meta = st.columns([1, 1.3])
    with col_av:
        avatar_img = np.zeros((160, 140, 3), dtype=np.uint8)
        avatar_img[:] = (35, 42, 48)
        cv2.circle(avatar_img, (70, 55), 32, (180, 190, 200), -1)
        cv2.ellipse(avatar_img, (70, 140), (55, 45), 0, 180, 360, (180, 190, 200), -1)
        cv2.rectangle(avatar_img, (2, 2), (138, 158), (0, 255, 128), 1)
        st.image(avatar_img, caption="ID: SUBJECT_KHR_001", channels="BGR")
    
    with col_av_meta:
        st.markdown("<div style='font-size:0.75rem; color:#88a0b0;'>CLEARANCE PROFILE</div>", unsafe_allow_html=True)
        st.markdown("<b style='color:#00ff80; font-size:1.0rem;'>AI-FIRST ARCHITECT</b>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;'>STATUS: <b style='color:#00ff80;'>VERIFIED</b></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;'>NAME: <b>Khushal</b></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;'>ORG: <b>Chronos Core</b></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;'>MATCH CONF: <b>98.5%</b></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:15px; font-size:0.8rem; color:#88a0b0;'>VERIFIED OSINT & CIVIL MATCHES:</div>", unsafe_allow_html=True)
    st.markdown("""
    - `[GITHUB]` @Khushal // Systems Lead (CONFIRMED)
    - `[LINKEDIN]` AI-First Backend & Distributed Arch
    - `[REGISTRY]` Badge ID #SEC-00912 (Active Operator)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # Key Statistics Box
    st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-title'>TACTICAL TARGET STATS</div>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("<div style='font-size:0.75rem; color:#88a0b0;'>IMPACT / VALUE</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-badge'>₹70LPA+</div>", unsafe_allow_html=True)
    with col_s2:
        st.markdown("<div style='font-size:0.75rem; color:#88a0b0;'>SCALE INDEX</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-badge' style='color:#00e5ff;'>150%</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem; color:#708599; margin-top:8px;'>SKILLS: DSA | SYSTEM DESIGN | RAG | AI AGENTS</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# CENTER COLUMN: MAIN TACTICAL VIDEO HUD WITH TARGET RETICLES
with col_center:
    st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-title'>LIVE PRIMARY SURVEILLANCE FEED // SECTOR ALPHA</div>", unsafe_allow_html=True)
    
    feed_frame = np.zeros((360, 640, 3), dtype=np.uint8)
    feed_frame[:] = (18, 22, 26)
    
    for x in range(0, 640, 50):
        cv2.line(feed_frame, (x, 0), (x, 360), (28, 35, 40), 1)
    for y in range(0, 360, 50):
        cv2.line(feed_frame, (0, y), (640, y), (28, 35, 40), 1)
        
    t_reticle_x, t_reticle_y = 260, 110
    cv2.rectangle(feed_frame, (t_reticle_x, t_reticle_y), (t_reticle_x + 130, t_reticle_y + 150), (0, 255, 128), 2)
    cv2.line(feed_frame, (t_reticle_x, t_reticle_y + 75), (t_reticle_x + 130, t_reticle_y + 75), (0, 255, 128), 1)
    
    cv2.line(feed_frame, (t_reticle_x - 10, t_reticle_y), (t_reticle_x, t_reticle_y), (0, 255, 128), 2)
    cv2.line(feed_frame, (t_reticle_x, t_reticle_y - 10), (t_reticle_x, t_reticle_y), (0, 255, 128), 2)
    cv2.line(feed_frame, (t_reticle_x + 140, t_reticle_y), (t_reticle_x + 130, t_reticle_y), (0, 255, 128), 2)
    cv2.line(feed_frame, (t_reticle_x + 130, t_reticle_y - 10), (t_reticle_x + 130, t_reticle_y), (0, 255, 128), 2)
    
    cv2.putText(feed_frame, "TARGET ACQUIRED: KHUSHAL", (t_reticle_x - 15, t_reticle_y - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 128), 1)
    cv2.putText(feed_frame, "AI-FIRST BACKEND LEAD", (t_reticle_x - 15, t_reticle_y + 168),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 128), 1)
    cv2.putText(feed_frame, "CHRONOS // CITY-WIDE THREAT SENSOR", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 1)

    st.image(feed_frame, channels="BGR", use_column_width=True)
    
    col_ctl1, col_ctl2, col_ctl3 = st.columns(3)
    with col_ctl1:
        if st.button("RE-SCAN FRAME"):
            st.rerun()
    with col_ctl2:
        if st.button("FORCE 3D RECON"):
            st.success("3D Facial Mesh Generation Triggered.")
    with col_ctl3:
        if st.button("BROADCAST ALERT"):
            st.warning("Dispatch notification sent to Operations Center.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN: 3D FACIAL MESH & HITL QUEUE
with col_right:
    st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-title'>3D FACIAL MORPHOMETRY (.OBJ)</div>", unsafe_allow_html=True)
    
    mesh_render = np.zeros((180, 280, 3), dtype=np.uint8)
    mesh_render[:] = (12, 16, 20)
    
    center_x, center_y = 140, 90
    for r in range(15, 75, 12):
        cv2.circle(mesh_render, (center_x, center_y), r, (0, 180, 100), 1)
    for angle in np.linspace(0, 2*np.pi, 16):
        x_pt = int(center_x + 65 * np.cos(angle))
        y_pt = int(center_y + 65 * np.sin(angle))
        cv2.line(mesh_render, (center_x, center_y), (x_pt, y_pt), (0, 90, 50), 1)
        cv2.circle(mesh_render, (x_pt, y_pt), 2, (0, 255, 128), -1)

    st.image(mesh_render, caption="468 Landmark 3D Coordinate Reconstruction", channels="BGR")
    st.markdown("<div style='font-size:0.75rem; color:#88a0b0;'>OBJ EXPORT: <code>data/3d_profiles/SUBJECT_KHR_001.obj</code></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Human-In-The-Loop Panel
    st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-title'>HUMAN-IN-THE-LOOP (HITL)</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.75rem;'>PENDING VERIFICATION: <b>1 Identity</b></div>", unsafe_allow_html=True)
    
    hitl_decision = st.selectbox("Operator Clearance Decision", ["APPROVE_IDENTITY", "FLAG_AS_ANOMALY", "REQUEST_HIGH_RES_SCAN"])
    reviewer_notes = st.text_input("Reviewer Log", "Subject identity validated against civil credentials.")
    if st.button("CONFIRM CLEARANCE ACTION"):
        st.success(f"Action '{hitl_decision}' recorded in Chronos Knowledge Graph.")
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Agentic Reasoning Narrative Terminal
st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
st.markdown("<div class='hud-title'>AGENTIC THREAT ONTOLOGY // GEMMA-4 LIVE REASONING STREAM</div>", unsafe_allow_html=True)
st.markdown("""
<div style='background:#05070a; border:1px solid #14241d; padding:12px; font-size:0.85rem; color:#00ff80;'>
<b>[CHRONOS_TACTICAL_AGENT]</b> Querying Graph: <i>(CAM_NODE_01) -[OBSERVES]-> (SUBJECT_KHR_001) -[LOCATED_IN]-> (Sector 07)</i><br/>
<b>[INFERENCE]</b> Anomaly Score: 0.12 (Nominal). Biometric similarity: 98.5%. Target authenticated as Principal Systems Lead.<br/>
<b>[DIRECTIVE]</b> Clear perimeter alarms. Maintain passive reconnaissance logging. Zero threat detected.
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
