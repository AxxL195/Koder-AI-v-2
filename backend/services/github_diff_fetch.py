from fastapi import HTTPException
import httpx

async def fetch_diff(diff_url: str,installation_token:str) -> str:
  
    headers= {
        'Accept': 'application/vnd.github+json',
        'Authorization' : f'Bearer {installation_token}'
    }

    async  with httpx.AsyncClient(follow_redirects=True) as client:
        response= await client.get(diff_url,headers=headers)
    
    # print(response.text)
    
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch diff. Status: {response.status_code}"
        )

    return response.text