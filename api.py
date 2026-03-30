from fastapi import FastAPI, Request
from security import analyze_event
from actions import auto_response

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    ip = data.get("ip", "unknown")
    event = data.get("event", "")

    threats, score, level = analyze_event(event, ip)
    actions = auto_response(ip, threats, score, level)

    return {
        "ip": ip,
        "threats": threats,
        "risk": score,
        "level": level,
        "actions": actions
    }
