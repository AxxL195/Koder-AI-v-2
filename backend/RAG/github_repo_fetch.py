from services.github_auth import get_installation_token
from services.github_fetch_repo import fetch_repo_details
import httpx

async def fetch_github_files(payload:dict):
    repo_full_name = payload['repositories'][0]['full_name']
    owner, repo = repo_full_name.split('/')
    installation_id = payload['installation']['id']

    installation_token = await get_installation_token(installation_id)

    repo_details = await fetch_repo_details(owner, repo, installation_token)
    branch = repo_details['default_branch'] 

    headers= {
        'Accept': 'application/vnd.github+json',
        'Authorization' : f'Bearer {installation_token}'
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1",
            headers=headers
        )

    print(response.json())