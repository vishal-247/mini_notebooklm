import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api

# Create an Inngest client
inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)

app = FastAPI()

# inngest function
@inngest_client.create_function(
    fn_id="Rag: Inngest pdf",
    trigger=inngest.TriggerEvent(event="rag/inngest_pdf")
)
async def rag_inngest_pdf(ctx:inngest.Context):
    return {"message": "Hello from Inngest!"}


# Serve the Inngest endpoint
inngest.fast_api.serve(app, inngest_client,functions=[rag_inngest_pdf])