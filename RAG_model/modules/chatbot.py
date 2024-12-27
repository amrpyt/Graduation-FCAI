from typing import List, Optional
from .embeddings import EmbeddingsModel
from .vector_store import VectorStore
from .file_handlers import DocumentProcessor

class RAGChatbot:
    def __init__(self):
        self.embeddings_model = EmbeddingsModel()
        self.vector_store = VectorStore()
        self.document_processor = DocumentProcessor()
        self.context_window = 5  # Number of relevant documents to consider

    def ingest_document(self, file_path: str) -> bool:
        """Process and ingest a document into the vector store."""
        try:
            # Process the document into chunks
            chunks = self.document_processor.process_file(file_path)
            
            # Generate embeddings for each chunk
            embeddings = [self.embeddings_model.get_embeddings(chunk) for chunk in chunks]
            
            # Store documents and embeddings
            self.vector_store.add_documents(chunks, embeddings)
            return True
        except Exception as e:
            raise Exception(f"Error ingesting document: {str(e)}")

    def get_relevant_context(self, query: str) -> List[str]:
        """Retrieve relevant context for the query."""
        try:
            # Generate embedding for the query
            query_embedding = self.embeddings_model.get_embeddings(query)
            
            # Search for relevant documents
            results = self.vector_store.search(query_embedding, limit=self.context_window)
            
            # Extract just the text from the results
            context = [text for text, _ in results]
            return context
        except Exception as e:
            raise Exception(f"Error getting relevant context: {str(e)}")

    def generate_response(self, query: str, context: Optional[List[str]] = None) -> str:
        """Generate a response using the query and optional context."""
        try:
            if context is None:
                context = self.get_relevant_context(query)
            
            # Construct the prompt with context
            prompt = self._construct_prompt(query, context)
            
            # Generate response using the embeddings model
            response = self.embeddings_model.get_completion(prompt)
            return response
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def _construct_prompt(self, query: str, context: List[str]) -> str:
        """Construct a prompt using the query and context."""
        context_str = "\n\n".join(context)
        prompt = f"""Context information is below.
---------------------
{context_str}
---------------------
Given the context information and no other information, answer the following query:
Query: {query}
Answer: """
        return prompt

    def chat(self, query: str) -> str:
        """Main chat interface that handles the entire RAG pipeline."""
        try:
            # Get relevant context
            context = self.get_relevant_context(query)
            
            # Generate response
            response = self.generate_response(query, context)
            
            return response
        except Exception as e:
            raise Exception(f"Error in chat: {str(e)}")
