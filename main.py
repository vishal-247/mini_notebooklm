import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from data_loader import load_and_chunk_pdf, get_embedding
from vector_db import QdrantStorage
import os
import uuid
import datetime
from dotenv import load_dotenv
from custom_types import RAGChunkAndSrc, RAGUpsertResult, RAGSearchResult, RAGQueryResult





# Create an Inngest client
inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)


# inngest function
@inngest_client.create_function(
    fn_id="Rag: Inngest pdf",
    trigger=inngest.TriggerEvent(event="rag/inngest_pdf")
)

# -------------------------------------
async def rag_inngest_pdf(ctx:inngest.Context):
    file_path=ctx.event.data.get("file_path")
    if not file_path:
        raise ValueError("file_path is required in event data")
    
    # Load and chunk the PDF
    chunks=load_and_chunk_pdf(file_path)
    if not chunks:
        raise ValueError("No text found in PDF")
    
    # Get embeddings for the chunks
    embeddings=get_embedding(chunks)
    
    # Upsert to Qdrant
    qdrant=QdrantStorage()
    points=[RAGChunkAndSrc(id=str(uuid.uuid4()),vector=emb, payload={"text":chunk,"source":file_path}) for chunk,emb in zip(chunks,embeddings)]
    qdrant.client.upsert(collection_name=qdrant.collection, points=points)
    
# -------------------------------------    


app = FastAPI()
# Serve the Inngest endpoint
inngest.fast_api.serve(app, inngest_client,functions=[rag_inngest_pdf])
