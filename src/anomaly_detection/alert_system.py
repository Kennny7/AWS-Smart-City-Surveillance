# src/anomaly_detection/alert_system.py

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =======================
# 1. LOAD ALERT CONFIG
# =======================
def load_alert_config(config_path='config/alert_config.json'):
    """
    Loads alert system configuration, e.g., email settings, Slack webhook, etc.
    """
    with open(config_path) as f:
        config = json.load(f)
    return config

# =======================
# 2. SEND EMAIL ALERT
# =======================
def send_email_alert(subject, body, email_config):
    """
    Sends an email alert using the provided configuration.
    """
    msg = MIMEMultipart()
    msg['From'] = email_config['sender']
    msg['To'] = email_config['recipient']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.ehlo()
        if email_config.get('use_tls'):
            server.starttls()
        server.login(email_config['username'], email_config['password'])
        server.sendmail(email_config['sender'], email_config['recipient'], msg.as_string())

# =======================
# 3. PROCESS ANOMALY EVENT
# =======================
def process_anomaly_event(anomaly_message):
    """
    Placeholder logic to handle an anomaly event.
    Could trigger multiple alert channels.
    """
    # Load alert config
    config = load_alert_config()
    email_config = config.get('email', {})

    # Construct alert details
    subject = "Anomaly Detected!"
    body = f"Alert: {anomaly_message}"

    # Send an email (if configured)
    if email_config:
        send_email_alert(subject, body, email_config)

    # Placeholder for other channels (e.g., Slack, logs)
    # if 'slack_webhook' in config:
    #     send_slack_alert(...)
    # else:
    #     log_to_file(anomaly_message)
