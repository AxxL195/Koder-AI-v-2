import time
import jwt
from config import PRIVATE_KEY
from config import APP_ID
import httpx
def generate_jwt_token() -> str:
    with open(PRIVATE_KEY, 'r') as f:
        private_key=f.read()
    
    current_time= int(time.time())
    payload = {
        "iss" : APP_ID,
        "iat":  current_time- 60,                   
        "exp":  current_time + 600
    }

    token = jwt.encode(payload,private_key,algorithm="RS256")

    return token


async def get_installation_token(installation_id:int) -> str:
    jwt_token= generate_jwt_token()

    # print(f"jwt_token : {jwt_token}")

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept':'application/vnd.github+json'
    }

    async with httpx.AsyncClient() as client:
        response =  await client.post(
            f'https://api.github.com/app/installations/{installation_id}/access_tokens',
            headers=headers
        )
    
        if response.status_code != 201:
            raise Exception(f"failed to get the installation token:{response.text}")

    response=response.json()

    return response["token"]

