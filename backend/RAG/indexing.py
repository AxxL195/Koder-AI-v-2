import httpx
import base64

from RAG.chunking import PreparedChunk, chunking_text
from RAG.embedding import embed_chunks
from services.language_finder import language_find
from services.filter import should_index
from RAG.vector_store import get_existing_blob_sha, store_chunks,delete_stale_chunks

async def file_index(owner:str,repo:str,installation_token:str,installation_id: int,files: list) :
    # print(files)
    headers= {
        'Authorization': f'Bearer {installation_token}',
        'Accept': 'application/vnd.github+json'
    }
    all_chunks= []
    repo_id=f"{owner}/{repo}"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        for file in files:
            file_path=file['path']
            file_type=file['type']

            if(should_index(file_path,file_type)):
                new_sha = file['sha']
                existing_sha = get_existing_blob_sha(repo_id,file_path)

                if existing_sha == new_sha:
                    # File hasn't changed — skip it entirely
                    print("unchanged, skipping:", file_path)
                    continue
                
                if existing_sha is not None:
                # File changed — delete old chunks before re-indexing
                    delete_stale_chunks(repo_id, file_path)
                
                response = await client.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}",headers= headers)

                file_data=response.json()

                raw_text= base64.b64decode(file_data['content']).decode('utf-8')

                language= language_find(file_data['name'])

                chunks=chunking_text(raw_text,file_path,language,file_type,file['sha'],repo_id,installation_id)

                all_chunks.extend(chunks)

            else:
                print("skipped :", file_path )

        if not all_chunks:
            print("Nothing to embed")
            return
        
        embedded= await embed_chunks(all_chunks)

        #store in pg vector
        store_chunks(embedded)

        print(f"indexed {len(embedded)} chunks for {repo_id}")


                
            