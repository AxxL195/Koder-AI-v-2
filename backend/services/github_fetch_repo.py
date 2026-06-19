import httpx

async def fetch_repo_details (owner:str, repo:str , installation_token:str) -> dict:
    headers = {
        'Accept' : 'application/vnd.github+json',
        'Authorization' :  f'Bearer {installation_token}'
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response= await client.get(f"https://api.github.com/repos/{owner}/{repo}",headers=headers)
    
    if(response.status_code!=200):
        print(f'Failed : {response.status_code}')
        return {}
    
    return response.json()