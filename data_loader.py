from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"
EMBED_DIM = 3072

splitter=SentenceSplitter(chunk_size=1000,chunk_overlap=200)


def load_and_chunk_pdf(file_path: str):
    docs=PDFReader().load_data(file=file_path)
    texts=[d.text for d in docs if getattr(d,'text',None)]
    chunks=[]
    for text in texts:
        chunks.extend(splitter.split(text)) 
    return chunks
def get_embedding(text:list[str])->list[list[float]]:
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return [e.embedding for e in response.data]