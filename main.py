from fastapi import FastAPI
from supabase import create_client, Client
import os

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/users")
async def get_users():
    res = supabase.table("users").select("*").execute()
    return res.data