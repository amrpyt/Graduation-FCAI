# RAG Chatbot with Gemini and Qdrant

A Retrieval-Augmented Generation (RAG) chatbot that uses Google's Gemini for embeddings and text generation, and Qdrant for vector storage. This implementation supports various document types including PDF, TXT, and Excel files.

## Features

- Document ingestion and processing (PDF, TXT, XLSX)
- Semantic search using Qdrant vector store
- Context-aware responses using Google's Gemini model
- Automatic text chunking and embedding generation
- Web interface with Streamlit
- Command-line interface

## Prerequisites

- Python 3.8+
- Qdrant server (local or cloud)
- Google API key for Gemini

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
GOOGLE_API_KEY=your_google_api_key
QDRANT_URL=your_qdrant_url  # default: http://localhost:6333
```

## Usage

### Web Interface (Recommended)
1. Start the web interface:
```bash
streamlit run RAG_model/app.py
```

2. Open your browser and navigate to the provided URL (usually http://localhost:8501)
3. Use the sidebar to upload documents
4. Start chatting with the bot in the main interface

### Command Line Interface
1. Start the CLI:
```bash
python RAG_model/main.py
```

2. Ingest documents:
```
You: ingest path/to/your/document.pdf
```

3. Chat with the bot:
```
You: What is the main topic of the document?
Assistant: [Response based on the document content]
```

4. Type 'quit' to exit the application.

## Supported File Types

- PDF (.pdf)
- Text files (.txt)
- Excel files (.xlsx)
- Word documents (.docx)

## Architecture

The system consists of several modules:

- `chatbot.py`: Main RAG pipeline implementation
- `embeddings.py`: Handles embedding generation using Gemini
- `vector_store.py`: Manages Qdrant vector store operations
- `file_handlers.py`: Processes different document types
- `app.py`: Streamlit web interface

## Error Handling

The system includes comprehensive error handling for:
- Missing environment variables
- File not found errors
- Document processing errors
- API communication errors
- Vector store operations

## Contributing

Feel free to submit issues and enhancement requests!
