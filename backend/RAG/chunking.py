from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

def chunking_text(text:str,language:str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=language,
        chunk_size=300,
        chunk_overlap=0,
    )

    chunks = splitter.split_text(text)

    print(chunks)