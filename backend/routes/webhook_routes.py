from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from RAG.github_repo_fetch import fetch_github_files
from controllers.webhook_controllers import process_webhook
from services.verify_signature import verify_signature

webhook_router= APIRouter()

@webhook_router.post('/github')
async def handle_webhook (request:Request , background_tasks:BackgroundTasks) -> dict:
    body = await request.body()

    event_type =  request.headers.get('X-GitHub-Event')

    signature = request.headers.get('X-Hub-Signature-256','')

    if not verify_signature(body,signature):
        raise HTTPException(status_code = 401, detail = "Invalid Signature")

    print("valid signature")

    payload = await request.json()
    
    if event_type == 'installation':
        if payload['action'] == 'created':
            background_tasks.add_task(fetch_github_files,payload)

    elif event_type == 'pull_request':
        action = payload["action"]    
        if action not in ['opened','synchronize','reopened']:
            print("status :","ignored")
            return {"status":"ignored"}
    
        background_tasks.add_task(process_webhook,payload)

        print("status :","queued")

        return {"status":"queued"}
    
    elif event_type=='push':
        if payload['ref'] == 'refs/heads/main':
            background_tasks.add_task()

    return {"status":"ok"}



