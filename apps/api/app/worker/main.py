"""Durable worker entry point. Database functions in the SQL migration own leasing and fencing."""
import asyncio, os, socket
from datetime import datetime, timezone

async def run():
    if os.getenv("AI_MODE","demo")=="demo":
        print("Worker idle: demo mode uses synthetic fixtures and makes no provider calls")
        return
    raise RuntimeError("Live worker requires Supabase configuration and applied migrations")
if __name__=="__main__": asyncio.run(run())
