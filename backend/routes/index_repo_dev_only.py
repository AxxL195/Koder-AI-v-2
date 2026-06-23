import httpx
from fastapi import APIRouter, status
from fastapi import BackgroundTasks

from controllers.process_installation_webhook import fetch_repo
from services.github_fetch_repo import fetch_repo_details
from services.github_auth import get_installation_token

dev_router = APIRouter()

@dev_router.post('/index_repo')
async def manual_index(background_tasks: BackgroundTasks):
    owner = "Axxl195"
    repo = "She-Can"
    installation_id = 139609824

    installation_token = await get_installation_token(installation_id)

    background_tasks.add_task(fetch_repo,owner,repo,installation_token,installation_id)
    
    return {"status": "indexing started"}