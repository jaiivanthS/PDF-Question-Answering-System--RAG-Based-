"""
Streamlit UI for PDF Question Answering System

This is the main user interface for uploading PDFs and asking questions.
"""

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
from pathlib import Path
import os

# Get the project root directory (3 levels up from this file)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

import streamlit as st
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pdf_rag.core.pdf_loader import PDFLoader
from pdf_rag.core.embeddings import EmbeddingGenerator
from pdf_rag.core.vector_store import VectorStore
from pdf_rag.core.retriever import RAGRetriever
from pdf_rag.models.llm_config import OpenRouterLLM
from pdf_rag.models.prompt_templates import PromptTemplates
from pdf_rag.utils.text_processing import TextProcessor
from pdf_rag.utils.config_loader import ConfigLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="PDF Question Answering System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'embedding_generator' not in st.session_state:
    st.session_state.embedding_generator = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def initialize_components():
    """Initialize RAG components."""
    try:
        # Load configurations
        config_loader = ConfigLoader()
        model_config = config_loader.load_config("model_config.yaml")
        rag_config = config_loader.load_config("rag_config.yaml")
        
        # Initialize embedding generator
        if st.session_state.embedding_generator is None:
            with st.spinner("Loading embedding model..."):
                st.session_state.embedding_generator = EmbeddingGenerator(
                    model_name=model_config['embeddings']['model_name'],
                    device=model_config['embeddings'].get('device', 'cpu')
                )
        
        # Initialize vector store
        if st.session_state.vector_store is None:
            st.session_state.vector_store = VectorStore(
                persist_directory=rag_config['vector_store']['persist_directory'],
                collection_name=rag_config['vector_store']['collection_name'],
                distance_metric=rag_config['vector_store'].get('distance_metric', 'cosine')
            )
        
        # Initialize LLM
        if st.session_state.llm is None:
            st.session_state.llm = OpenRouterLLM(
                model_name=model_config['llm']['model_name'],
                temperature=model_config['llm']['temperature'],
                max_tokens=model_config['llm']['max_tokens'],
                app_name=model_config['openrouter'].get('app_name', 'PDF-RAG-QA-System')
            )
        
        # Initialize retriever
        if st.session_state.retriever is None:
            st.session_state.retriever = RAGRetriever(
                vector_store=st.session_state.vector_store,
                embedding_generator=st.session_state.embedding_generator,
                k=rag_config['retrieval']['k'],
                score_threshold=rag_config['retrieval']['score_threshold']
            )
        
        return True
        
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        logger.error(f"Initialization error: {str(e)}")
        return False


def process_pdf(uploaded_file):
    """Process uploaded PDF file."""
    try:
        # Load configurations
        config_loader = ConfigLoader()
        rag_config = config_loader.load_config("rag_config.yaml")
        
        # Save uploaded file temporarily
        temp_path = Path("data/raw") / uploaded_file.name
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load PDF
        with st.spinner("Extracting text from PDF..."):
            pdf_loader = PDFLoader()
            pdf_data = pdf_loader.load(str(temp_path))
        
        st.success(f"✅ Loaded PDF with {pdf_data['num_pages']} pages")
        
        # Process text
        with st.spinner("Chunking text..."):
            text_processor = TextProcessor(
                chunk_size=rag_config['document_processing']['chunk_size'],
                chunk_overlap=rag_config['document_processing']['chunk_overlap'],
                separators=rag_config['document_processing']['separators']
            )
            
            chunks = text_processor.split_text(pdf_data['text'])
        
        st.success(f"✅ Created {len(chunks)} text chunks")
        
        # Generate embeddings
        with st.spinner("Generating embeddings..."):
            embeddings = st.session_state.embedding_generator.embed_texts(
                chunks,
                show_progress=True
            )
        
        st.success(f"✅ Generated {len(embeddings)} embeddings")
        
        # Store in vector database
        with st.spinner("Storing in vector database..."):
            metadatas = [
                {
                    "source": uploaded_file.name,
                    "page_count": pdf_data['num_pages'],
                    "chunk_index": i
                }
                for i in range(len(chunks))
            ]
            
            st.session_state.vector_store.add_documents(
                texts=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )
        
        st.success(f"✅ Stored {len(chunks)} chunks in vector database")
        st.session_state.documents_loaded = True
        
        return True
        
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        logger.error(f"PDF processing error: {str(e)}")
        return False


def answer_question(question: str):
    """Answer a question using RAG."""
    try:
        # Retrieve relevant documents
        with st.spinner("Retrieving relevant documents..."):
            retrieved_docs = st.session_state.retriever.retrieve(question)
        
        if not retrieved_docs:
            return "I couldn't find any relevant information in the uploaded documents to answer your question."
        
        # Format context
        context = st.session_state.retriever.format_context(retrieved_docs)
        
        # Generate answer
        with st.spinner("Generating answer..."):
            system_message = PromptTemplates.get_system_message("qa")
            answer = st.session_state.llm.generate_with_context(
                question=question,
                context=context,
                system_message=system_message
            )
        
        # Store in chat history
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "sources": retrieved_docs
        })
        
        return answer, retrieved_docs
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return f"Error generating answer: {str(e)}", []


# Main UI
def main():
    st.title("📚 PDF Question Answering System")
    st.markdown("Upload PDFs and ask questions about their content using RAG (Retrieval-Augmented Generation)")
    
    # Initialize components
    if not initialize_components():
        st.stop()
    
    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📄 Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file is not None:
            if st.button("Process PDF", type="primary"):
                process_pdf(uploaded_file)
        
        st.divider()
        
        # Show database stats
        st.header("📊 Database Stats")
        doc_count = st.session_state.vector_store.get_collection_count() if st.session_state.vector_store else 0
        st.metric("Documents in Database", doc_count)
        
        if doc_count > 0:
            if st.button("Clear Database", type="secondary"):
                st.session_state.vector_store.reset_collection()
                st.session_state.documents_loaded = False
                st.session_state.chat_history = []
                st.success("Database cleared!")
                st.rerun()
    
    # Main content area
    if not st.session_state.documents_loaded:
        st.info("👈 Please upload and process a PDF to get started")
    else:
        st.success("✅ Documents loaded! Ask questions below.")
        
        # Question input
        question = st.text_input("Ask a question about your documents:", placeholder="What is this document about?")
        
        if st.button("Get Answer", type="primary") and question:
            answer, sources = answer_question(question)
            
            # Display answer
            st.markdown("### Answer")
            st.markdown(answer)
            
            # Display sources
            if sources:
                with st.expander("📖 View Source Documents"):
                    for i, source in enumerate(sources):
                        st.markdown(f"**Source {i+1}** (Distance: {source['distance']:.3f})")
                        st.text(source['text'][:500] + "..." if len(source['text']) > 500 else source['text'])
                        st.divider()
        
        # Chat history
        if st.session_state.chat_history:
            st.divider()
            st.header("💬 Chat History")
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:100]}..."):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Answer:** {chat['answer']}")


if __name__ == "__main__":
    main()
