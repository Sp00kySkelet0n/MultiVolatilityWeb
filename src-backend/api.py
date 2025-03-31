from typing import Any
from fastapi import FastAPI, Body, Header, HTTPException
import json
import os
import hashlib
import requests

def discord_notification(dump_name,module_name):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    data = {
        "content": f"✅ Module {module_name} for {dump_name} is ready!",
        "username": "MultiVolBot"
    }
    try:
        response = requests.post(webhook_url, json=data)
    except:
        print("error")

    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

app = FastAPI()

SAFE_BASE = "/shared_volume"

def sha512_hash(text: str) -> str:
    return hashlib.sha512(text.encode("utf-8")).hexdigest()

@app.post("/receive-json/")
async def receive_json(
    payload: Any = Body(...),
    dump_name: str = Header(...),
    module_name: str = Header(...),
    api_password: str = Header(...)  # this is already hashed by the client
):
    # Get plain text password from environment and hash it
    local_password = os.getenv("API_PASSWORD")
    if not local_password:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_PASSWORD not set")

    local_password_hash = sha512_hash(local_password)

    if local_password_hash != api_password:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Write to /shared_volume/dump_name/module_name/output.json
    save_path = os.path.join(SAFE_BASE, dump_name, module_name)
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, "output.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

    discord_notification(dump_name,module_name)

    return {"status": "ok"}
