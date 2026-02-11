from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams,PointStruct



class QdrantStorage:
    def __init__(self,url="http://localhost:6333",collection="docs",dim=3072):
        self.client = QdrantClient(url=url,Timeout=30)
        self.collection = collection
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            )


    def search(self,query_vector,top_k=5):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k
        )
        contexts=[]
        sources=set()

        for r in results:
            payload = getattr(r, 'payload',None) or {}
            text=payload.get('text','')
            source=payload.get('source','')
            if text:
                contexts.append(text)
                sources.add(source)
        
        return {"contexts": contexts, "sources": list(sources)}