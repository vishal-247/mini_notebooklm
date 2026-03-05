# from openai import OpenAI
# from llama_index.readers.file import PDFReader
# from llama_index.core.node_parser import SentenceSplitter
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# EMBEDDING_MODEL = "text-embedding-3-small"
# EMBED_DIM = 3072

# splitter=SentenceSplitter(chunk_size=1000,chunk_overlap=200)


# def load_and_chunk_pdf(file_path: str):
#     docs=PDFReader().load_data(file=file_path)
#     texts=[d.text for d in docs if getattr(d,'text',None)]
#     chunks=[]

# # ------------------------------------------------
#     print(chunks)  #kuch to gadbad hai daya 
# #-------------------------------------------------    

#     for text in texts:
#         chunks.extend(splitter.split_text(text)) 
#     return chunks


# def get_embedding(text:list[str])->list[list[float]]:
#     response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
#     return [e.embedding for e in response.data]
















# from groq import Groq
# from llama_index.readers.file import PDFReader
# from llama_index.core.node_parser import SentenceSplitter
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# # EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# EMBEDDING_MODEL = "nomic-embed-text-v1.5"

# EMBED_DIM = 3072

# splitter=SentenceSplitter(chunk_size=1000,chunk_overlap=200)


# def load_and_chunk_pdf(file_path: str):
#     docs=PDFReader().load_data(file=file_path)
#     texts=[d.text for d in docs if getattr(d,'text',None)]
#     chunks=[]

# # ------------------------------------------------
#     print(chunks)  #kuch to gadbad hai daya 
# #-------------------------------------------------    

#     for text in texts:
#         chunks.extend(splitter.split_text(text)) 
#     return chunks


# def get_embedding(text:list[str])->list[list[float]]:
#     response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
#     return [e.embedding for e in response.data]





from groq import Groq
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

# Groq for LLM only
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Local embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

EMBED_DIM = 384  # MiniLM output size

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunk_pdf(file_path: str):
    docs = PDFReader().load_data(file=file_path)
    texts = [d.text for d in docs if getattr(d, "text", None)]

    chunks = []

    for text in texts:
        chunks.extend(splitter.split_text(text))

    print("Total chunks:", len(chunks))
    return chunks


def get_embedding(texts: list[str]) -> list[list[float]]:
    embeddings = embedding_model.encode(texts)
    return embeddings.tolist()