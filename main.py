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


# inngest function to handel pdf uplaod
@inngest_client.create_function(
    fn_id="Rag: pdf_upload_handdler",
    trigger=inngest.TriggerEvent(event="rag/inngest_upload_pdf")
)
async def rag_inngest_pdf(ctx: inngest.Context):
    
    file_path=ctx.event.data.get("file_path")
    if not file_path:
        raise ValueError("file_path is required in event data")
    
    
    chunks= load_and_chunk_pdf(file_path)
    if not chunks:
        raise ValueError("no text found in pdf")
    
    embeddings = get_embedding(chunks)


    

# -------------------------------------
# async def rag_inngest_pdf(ctx:inngest.Context):
#     file_path=ctx.event.data.get("file_path")
#     if not file_path:
#         raise ValueError("file_path is required in event data")
    
#     # Load and chunk the PDF
#     chunks=load_and_chunk_pdf(file_path)
#     if not chunks:
#         raise ValueError("No text found in PDF")
    
#     # Get embeddings for the chunks
#     embeddings=get_embedding(chunks)
    
    # Upsert to Qdrant
    # qdrant=QdrantStorage()
    # points=[RAGChunkAndSrc(id=str(uuid.uuid5()),vector=emb, payload={"text":chunk,"source":file_path}) for chunk,emb in zip(chunks,embeddings)]
    # qdrant.client.upsert(collection_name=qdrant.collection, points=points)
# async def rag_ingest_pdf(ctx: inngest.Context):
#     def _load(ctx: inngest.Context) -> RAGChunkAndSrc:
#         pdf_path = ctx.event.data["pdf_path"]
#         source_id = ctx.event.data.get("source_id", pdf_path)
#         chunks = load_and_chunk_pdf(pdf_path)
#         return RAGChunkAndSrc(chunks=chunks, source_id=source_id)

#     def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult:
#         chunks = chunks_and_src.chunks
#         source_id = chunks_and_src.source_id
#         vecs = get_embedding(chunks)
#         ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}:{i}")) for i in range(len(chunks))]
#         payloads = [{"source": source_id, "text": chunks[i]} for i in range(len(chunks))]
#         QdrantStorage().upsert(ids, vecs, payloads)
#         return RAGUpsertResult(ingested=len(chunks))

#     chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx), output_type=RAGChunkAndSrc)
#     ingested = await ctx.step.run("embed-and-upsert", lambda: _upsert(chunks_and_src), output_type=RAGUpsertResult)
#     return ingested.model_dump()



# -------------------------------------    


app = FastAPI()
# Serve the Inngest endpoint
inngest.fast_api.serve(app, inngest_client,functions=[rag_ingest_pdf])
