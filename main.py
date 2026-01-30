from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
from supabase import create_client, Client
import os
import json
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

class DragEvent(BaseModel):
    count: int
    user_id: str

class ActionConfig(BaseModel):
    trigger_count: int
    action_type: str
    action_data: Optional[Dict] = {}

class ConfigResponse(BaseModel):
    actions: List[ActionConfig]

class ActionResponse(BaseModel):
    action_type: str
    action_data: Optional[Dict] = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/config", response_model=ConfigResponse)
async def get_config():
    actions = [
        {
            "trigger_count": 20,
            "action_type": "show_welcome_text",
            "action_data": {
                "text": "欢迎来到乔雪源的世界",
                "duration": 5000
            }
        }
    ]
    return {"actions": actions}

@app.post("/api/drag")
async def report_drag(event: DragEvent):
    try:
        timestamp = datetime.now().isoformat()
        
        data = {
            "count": event.count,
            "user_id": event.user_id,
            "timestamp": timestamp
        }
        
        res = supabase.table("drag_events").insert(data).execute()
        
        return {"status": "success", "count": event.count, "user_id": event.user_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/actions/{count}", response_model=ActionResponse)
async def get_action(count: int):
    config = await get_config()
    
    for action in config["actions"]:
        if action["trigger_count"] == count:
            return {
                "action_type": action["action_type"],
                "action_data": action.get("action_data", {})
            }
    
    return {"action_type": "none", "action_data": {}}

@app.get("/api/user/{user_id}")
async def get_user_stats(user_id: str):
    try:
        res = supabase.table("drag_events").select("*").eq("user_id", user_id).execute()
        
        if not res.data:
            return {
                "user_id": user_id,
                "total_drags": 0,
                "max_count": 0,
                "first_drag": None,
                "last_drag": None
            }
        
        total_drags = len(res.data)
        max_count = max(event["count"] for event in res.data)
        first_drag = min(event["timestamp"] for event in res.data)
        last_drag = max(event["timestamp"] for event in res.data)
        
        return {
            "user_id": user_id,
            "total_drags": total_drags,
            "max_count": max_count,
            "first_drag": first_drag,
            "last_drag": last_drag
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/leaderboard")
async def get_leaderboard():
    try:
        res = supabase.table("drag_events").select("*").execute()
        
        user_stats = {}
        for event in res.data:
            user_id = event["user_id"]
            if user_id not in user_stats:
                user_stats[user_id] = {
                    "user_id": user_id,
                    "max_count": event["count"],
                    "total_drags": 1
                }
            else:
                user_stats[user_id]["max_count"] = max(user_stats[user_id]["max_count"], event["count"])
                user_stats[user_id]["total_drags"] += 1
        
        leaderboard = sorted(user_stats.values(), key=lambda x: x["max_count"], reverse=True)[:10]
        
        return {"leaderboard": leaderboard}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/users")
async def get_users():
    res = supabase.table("users").select("*").execute()
    return res.data