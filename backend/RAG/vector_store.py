import os
from supabase import create_client,Client

from config import SUPABASE_SERVICE_KEY, SUPABASE_URL

url= SUPABASE_URL
key=SUPABASE_SERVICE_KEY

supabase: Client =  create_client(url,key)

def delete_stale_chunks(repo_id:str,file_path:str):
    supabase.table("code_chunks") \
        .delete() \
        .eg("repo_id",repo_id) \
        .execute()

def store_chunks(embedded_chunks:list[dict]):
    supabase.table("code_chunks").insert(embedded_chunks).execute()

def get_existing_blob_sha(repo_id:str, file_path:str) -> str | None:
    result= supabase.table("code_chunks") \
        .select("blob_sha") \
        .eq("repo_id", repo_id) \
        .eq("file_path", file_path) \
        .limit(1) \
        .execute()

    if result.data:
        return result.data[0]["blob_sha"]
    return None