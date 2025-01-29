# src/web_dashboard/app.py

# =======================
# 1. IMPORTS
# =======================
from flask import Flask, render_template, request
import os

# =======================
# 2. FLASK APP SETUP
# =======================
app = Flask(__name__)

# =======================
# 3. HELPER: READ ANOMALIES
# =======================
def read_anomalies_from_log(log_path='logs/anomalies.log'):
    """
    Reads anomaly entries from a simple log file.
    Each line in the log file might contain a timestamp + anomaly info.
    """
    if not os.path.exists(log_path):
        return []
    with open(log_path, 'r') as f:
        lines = f.readlines()
    # Strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    return lines

# =======================
# 4. INDEX ROUTE
# =======================
@app.route('/')
def index():
    """
    Displays a basic dashboard with recent anomalies.
    """
    anomalies = read_anomalies_from_log()
    return render_template('index.html', anomalies=anomalies)

# =======================
# 5. RUN FLASK APP
# =======================
if __name__ == '__main__':
    # Note: In production, use a production server (e.g., gunicorn).
    app.run(host='0.0.0.0', port=5000, debug=True)
