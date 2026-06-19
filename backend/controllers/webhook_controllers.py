from fastapi import HTTPException
from services.github_auth import get_installation_token
from services.github_diff_fetch import fetch_diff
from services.ai_review import ai_review_diff
from services.github_push_review import push_review

async def process_webhook(payload: dict):
    print(payload)
    PR_number=  payload['pull_request']['number']
    diff_url =  payload['pull_request']["diff_url"]
    repo_full_name =  payload['repository']['full_name']
    installation_id = payload['installation']['id']
    head_SHA = payload['pull_request']['head']['sha']

    # check if repo has been indexed yet
    count = await db.fetch_done(
        "SELECT COUNT(*) FROM code_chunks WHERE repo_name = :repo",
        {"repo" : repo_full_name}
    )

    if count == 0:
        # vectors not ready yet — review without RAG context
        installation_token = await get_installation_token (installation_id)
        response = await fetch_diff(diff_url,installation_token)
        ai_review = await ai_review_diff(response,repo_full_name,PR_number)
    else:
        # vectors ready — full RAG review
        installation_token = await get_installation_token (installation_id)
        response = await fetch_diff(diff_url,installation_token)
        ai_review = await ai_review_diff(response,repo_full_name,PR_number)
    
    await push_review(ai_review,installation_token,repo_full_name,PR_number,head_SHA)
