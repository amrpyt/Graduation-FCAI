import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class EmbeddingsModel:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_embeddings(self, text):
        """Generate embeddings for the given text using Gemini."""
        try:
            response = self.model.generate_content(text)
            # Note: This is a placeholder as Gemini doesn't directly provide embeddings
            # We'll use sentence-transformers as a fallback
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(text)
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    def get_completion(self, prompt):
        """Get completion from Gemini model."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error getting completion: {str(e)}")
