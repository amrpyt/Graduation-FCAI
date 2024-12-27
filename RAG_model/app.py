import streamlit as st
import os
from pathlib import Path
from modules.chatbot import RAGChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stMarkdown {
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot and check for required environment variables."""
    required_vars = ["GOOGLE_API_KEY", "QDRANT_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.info("Please set them in your .env file")
        st.stop()
    
    return RAGChatbot()

def main():
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = initialize_chatbot()

    # Sidebar for document upload
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader("Upload a document", 
                                       type=["pdf", "txt", "xlsx", "docx"],
                                       help="Supported formats: PDF, TXT, XLSX, DOCX")
        
        if uploaded_file:
            try:
                # Save the uploaded file temporarily
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Ingest the document
                with st.spinner("Processing document..."):
                    st.session_state.chatbot.ingest_document(str(temp_path))
                st.success("Document successfully ingested!")
                
                # Clean up
                temp_path.unlink()
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

    # Main chat interface
    st.title("RAG Chatbot 🤖")
    st.markdown("Ask questions about your documents!")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.chat(prompt)
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main() 