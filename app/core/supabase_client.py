from dotenv import load_dotenv

load_dotenv()
import os

import httpx

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


class SupabaseREST:
    def __init__(self, url: str, key: str):
        self.url = url.rstrip("/")
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.Client(headers=self.headers, timeout=30)

    def get(self, table: str, params: dict = None):
        resp = self.client.get(f"{self.url}/rest/v1/{table}", params=params)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

    def post(self, table: str, data: dict):
        resp = self.client.post(f"{self.url}/rest/v1/{table}", json=data)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

    def patch(self, table: str, match: dict, data: dict):
        params = {f"{k}": f"eq.{v}" for k, v in match.items()}
        resp = self.client.patch(
            f"{self.url}/rest/v1/{table}", params=params, json=data
        )
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

    def delete(self, table: str, match: dict):
        params = {f"{k}": f"eq.{v}" for k, v in match.items()}
        resp = self.client.delete(f"{self.url}/rest/v1/{table}", params=params)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None


supabase = SupabaseREST(SUPABASE_URL, SUPABASE_KEY)
