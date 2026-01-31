from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import json
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        actions = [
            {
                "trigger_count": 20,
                "action_type": "show_welcome_text",
                "action_data": {
                    "text": "欢迎来到乔雪源的世界",
                    "duration": 5000
                }
            },
            {
                "trigger_count": 50,
                "action_type": "show_welcome_text",
                "action_data": {
                    "text": "你已经是宇宙探索者了！",
                    "duration": 3000
                }
            },
            {
                "trigger_count": 100,
                "action_type": "show_welcome_text",
                "action_data": {
                    "text": "宇宙的奥秘等待你发现",
                    "duration": 4000
                }
            }
        ]
        return {"actions": actions}

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