def analyze_event(event, ip):
    threats = []
    score = 0

    if not event:
        return [], 0, "LOW"

    event = event.lower()

    if "failed login" in event:
        threats.append("Brute Force")
        score += 30

    if "sql" in event or "' or 1=1" in event:
        threats.append("SQL Injection")
        score += 50

    if "malware" in event:
        threats.append("Malware")
        score += 70

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return threats, score, level
