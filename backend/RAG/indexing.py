import httpx
import base64

from RAG.chunking import chunking_text
from services.language_finder import language_find
from services.filter import should_index

async def file_index(owner:str,repo:str,installation_token:str,files: list):
    # print(files)
    headers= {
        'Authorization': f'Bearer {installation_token}',
        'Accept': 'application/vnd.github+json'
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # for file in files:
        #     file_path=file['path']
        #     file_type=file['type']
        #     if(should_index(file_path,file_type)):
        #         response = await client.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}",headers= headers)

        #         file_data=response.json()
        #         print(file_data)

        #         raw_text= base64.b64decode(file_data['content']).decode('utf-8')

        #         print(raw_text)

        file_path=files[4]['path']
        file_type=files[4]['type']
        if(should_index(file_path,file_type)):
            response = await client.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}",headers= headers)

            file_data=response.json()

            print(file_data)

            raw_text= base64.b64decode(file_data['content']).decode('utf-8')

            print(raw_text)

            language= language_find(file_data['name'])

            chunking_text(raw_text,language)

        else:
            print("skipped :", file_path )


                
            