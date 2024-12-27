import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=self.qdrant_url)
        self.collection_name = "documents"
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if it doesn't."""
        collections = self.client.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Size for all-MiniLM-L6-v2 embeddings
                    distance=models.Distance.COSINE
                )
            )

    def add_documents(self, documents, embeddings):
        """Add documents and their embeddings to the vector store."""
        try:
            points = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                points.append(models.PointStruct(
                    id=i,
                    vector=embedding.tolist(),
                    payload={"text": doc}
                ))
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            raise Exception(f"Error adding documents to vector store: {str(e)}")

    def search(self, query_embedding, limit=5):
        """Search for similar documents using the query embedding."""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=limit
            )
            return [(hit.payload["text"], hit.score) for hit in results]
        except Exception as e:
            raise Exception(f"Error searching vector store: {str(e)}")

    def delete_collection(self):
        """Delete the collection."""
        try:
            self.client.delete_collection(self.collection_name)
            return True
        except Exception as e:
            raise Exception(f"Error deleting collection: {str(e)}")
