import os
import httpx
from config import GEMINI_API_KEY

EMBED_URL= (
    "https://generativelanguage.googleapis.com/v1beta"
    "/models/gemini-embedding-001:batchEmbedContents"
)

BATCH_SIZE = 20

async def embed_chunks(chunks:list) -> list[dict]:
    results= []

    for batch_start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[batch_start : batch_start + BATCH_SIZE]
        requests= [
            {
                "model":"model/gemini-embedding-001",
                "content":{
                    "parts":[{"text":chunk.text}]
                },
                "taskType": "RETRIEVAL_DOCUMENT",
                "outputDimensionality": 768   # Matryoshka truncation
            }
            for chunk in batch
        ]

        async with httpx.AsyncClient() as client:
            response = await  client.post(
                EMBED_URL,
                headers={"x-goog-api-key":GEMINI_API_KEY},
                json={"requests":request},
                timeout=30.0
            )

            response.raise_for_status()
            data=response.json()
        for chunk, embedding_obj in zip(batch, data["embeddings"]):
            vector = embedding_obj["values"]  

            # This dict maps directly to your pgvector table columns
            results.append({
                "repo_id":          chunk.repo_id,
                "installation_id":  chunk.installation_id,
                "file_path":        chunk.file_path,
                "file_type":        chunk.file_type,
                "language":         chunk.language,
                "blob_sha":         chunk.blob_sha,
                "chunk_index":      chunk.chunk_index,
                "text":             chunk.text,
                "embedding":        vector,   # the actual vector
            })
    return results