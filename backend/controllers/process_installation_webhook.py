from RAG.indexing import file_index
from services.github_fetch_repo import fetch_repo_details
import httpx

async def fetch_repo(owner:str,repo:str,installation_token:str):
    repo_details =  await fetch_repo_details(owner,repo,installation_token)
    branch= repo_details['default_branch']

    # print(f"branch:{branch}")

    headers= {
        'Accept': 'application/vnd.github+json',
        'Authorization' : f'Bearer {installation_token}'
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1",
            headers=headers
        )

    files=response.json()['tree']

    await file_index(owner,repo,installation_token,files)
    
   