from utils import send_telegram_alert, send_email_alert, block_ip

SIMULATION_MODE = True

def auto_response(ip, threats, score, level):
    actions = []

    if "SQL Injection" in threats:
        actions.append("🚫 Block IP")

    if "Brute Force" in threats:
        actions.append("🔐 Lock Account")

    if "Malware" in threats:
        actions.append("🦠 Quarantine File")

    message = f"""
🚨 SECURITY ALERT
IP: {ip}
Threats: {threats}
Risk: {score} ({level})
Actions: {actions}
"""

    send_telegram_alert(message)
    send_email_alert(message)

    if not SIMULATION_MODE and "🚫 Block IP" in actions:
        block_ip(ip)

    return actions
