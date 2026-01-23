"""
Main Application for PDF RAG Question-Answering System with Ollama
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pdf_loader import PDFLoader
from rag import RAGSystem


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Get Ollama URL from env or use default
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    llm_model = os.getenv("LLM_MODEL", "mistral")
    
    return ollama_url, embedding_model, llm_model


def initialize_system(data_dir: str = "data", 
                     vector_store_dir: str = "vector_store",
                     ollama_url: str = "http://localhost:11434",
                     embedding_model: str = "nomic-embed-text",
                     llm_model: str = "mistral"):
    """
    Initialize PDF Loader and RAG System
    
    Args:
        data_dir: Directory containing PDF files
        vector_store_dir: Directory to store/load vector embeddings
        ollama_url: URL of Ollama server
        embedding_model: Embedding model to use
        llm_model: LLM model to use
        
    Returns:
        Tuple of (pdf_loader, rag_system)
    """
    # Initialize PDF Loader
    pdf_loader = PDFLoader(chunk_size=1000, chunk_overlap=200)
    
    # Load PDFs from data directory
    documents = pdf_loader.load_pdfs_from_directory(data_dir)
    
    if not documents:
        print(f"Warning: No documents found in {data_dir}")
        return pdf_loader, None
    
    # Initialize RAG System with Ollama
    try:
        rag_system = RAGSystem(
            ollama_base_url=ollama_url,
            embedding_model=embedding_model,
            llm_model=llm_model
        )
    except ConnectionError as e:
        print(f"Error: {str(e)}")
        return pdf_loader, None
    
    # Build vector store
    vector_store_path = os.path.join(vector_store_dir, "faiss_index")
    os.makedirs(vector_store_dir, exist_ok=True)
    
    rag_system.build_vector_store(documents, vector_store_path)
    rag_system.setup_qa_chain()
    
    return pdf_loader, rag_system


def interactive_qa_session(rag_system: RAGSystem):
    """
    Run interactive Q&A session
    
    Args:
        rag_system: Initialized RAG System
    """
    if not rag_system:
        print("RAG System not initialized. Cannot start Q&A session.")
        return
    
    print("\n" + "="*60)
    print("PDF RAG Question-Answering System (Ollama)")
    print("="*60)
    print("Enter your questions about the PDF documents.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            question = input("Your question: ").strip()
            
            if question.lower() == 'exit':
                print("Goodbye!")
                break
            
            if not question:
                print("Please enter a valid question.\n")
                continue
            
            print("\nProcessing your question...")
            result = rag_system.answer_question(question)
            
            print(f"\nAnswer: {result['answer']}")
            
            if result['sources']:
                print("\nSource Documents:")
                for i, doc in enumerate(result['sources'], 1):
                    print(f"  {i}. {doc.metadata.get('source', 'Unknown')}")
            
            print("\n" + "-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error processing question: {str(e)}\n")


def batch_qa(rag_system: RAGSystem, questions: list):
    """
    Process a batch of questions
    
    Args:
        rag_system: Initialized RAG System
        questions: List of questions to answer
    """
    if not rag_system:
        print("RAG System not initialized.")
        return
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        result = rag_system.answer_question(question)
        results.append(result)
        print(f"Answer: {result['answer']}\n")
    
    return results


def main():
    """Main entry point"""
    
    # Load environment configuration
    ollama_url, embedding_model, llm_model = load_environment()
    
    # Get current directory paths
    current_dir = Path(__file__).parent
    data_dir = str(current_dir / "data")
    vector_store_dir = str(current_dir / "vector_store")
    
    print("Initializing RAG System with Ollama...")
    print(f"Ollama URL: {ollama_url}")
    print(f"Embedding Model: {embedding_model}")
    print(f"LLM Model: {llm_model}\n")
    
    pdf_loader, rag_system = initialize_system(
        data_dir,
        vector_store_dir,
        ollama_url,
        embedding_model,
        llm_model
    )
    
    if not rag_system:
        print("Failed to initialize RAG System. Please check Ollama is running.")
        return
    
    print("RAG System initialized successfully!\n")
    
    # Start interactive session
    interactive_qa_session(rag_system)


if __name__ == "__main__":
    main()
