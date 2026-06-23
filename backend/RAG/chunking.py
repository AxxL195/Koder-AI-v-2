from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

@dataclass
class PreparedChunk:
    text:str

    file_path:str
    file_type:str
    language:str
    blob_sha:str
    chunk_index:int

    repo_id:str
    installation_id:int

def chunking_text(text:str,file_path:str,language:str,file_type:str,blob_sha:str,repo_id:str,installation_id:int) -> list[PreparedChunk]:
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=language,
        chunk_size=512,
        chunk_overlap=50,
    )

    chunks:list[str] = splitter.split_text(text)

    prepared_chunks = []

    for chunk_index,chunk_text in enumerate(chunks):
        chunk= PreparedChunk(
            text=chunk_text,
            file_path = file_path,
            language=language,
            file_type=file_type,
            blob_sha=blob_sha,
            chunk_index=chunk_index,
            repo_id=repo_id,
            installation_id=installation_id,
        )

        prepared_chunks.append(chunk)
    return prepared_chunks