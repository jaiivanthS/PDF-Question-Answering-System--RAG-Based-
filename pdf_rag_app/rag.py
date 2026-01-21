"""
RAG (Retrieval-Augmented Generation) System with Ollama
Combines vector retrieval with local LLM for Q&A
"""

from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os
import requests


class RAGSystem:
    """RAG System for PDF Question Answering using Ollama"""
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", 
                 embedding_model: str = "nomic-embed-text",
                 llm_model: str = "mistral"):
        """
        Initialize RAG System with Ollama
        
        Args:
            ollama_base_url: URL where Ollama is running
            embedding_model: Model for embeddings (default: nomic-embed-text)
            llm_model: Model for chat (default: mistral)
        """
        self.ollama_base_url = ollama_base_url
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        
        # Check if Ollama is running
        self._check_ollama_connection()
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            base_url=ollama_base_url,
            model=embedding_model
        )
        
        # Initialize LLM
        self.llm = Ollama(
            base_url=ollama_base_url,
            model=llm_model,
            temperature=0.7
        )
        
        self.vector_store = None
        self.qa_chain = None
        
        # Custom prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Use the following context to answer the question. 
If you don't know the answer from the context, say "I don't have enough information".

Context: {context}

Question: {question}

Answer:"""
        )
    
    def _check_ollama_connection(self) -> None:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Connected to Ollama at {self.ollama_base_url}")
            else:
                raise ConnectionError(f"Ollama returned status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.ollama_base_url}. "
                f"Make sure Ollama is running: ollama serve"
            )
        except Exception as e:
            raise ConnectionError(f"Error connecting to Ollama: {str(e)}")
    
    def build_vector_store(self, documents: List, vector_store_path: str = None) -> None:
        """
        Build or load vector store from documents
        
        Args:
            documents: List of document chunks
            vector_store_path: Path to save/load vector store
        """
        print("Building vector store from documents...")
        
        if vector_store_path and os.path.exists(vector_store_path):
            print(f"Loading existing vector store from {vector_store_path}")
            self.vector_store = FAISS.load_local(vector_store_path, self.embeddings)
        else:
            if not documents:
                raise ValueError("No documents provided to build vector store")
            
            print(f"Creating embeddings for {len(documents)} document chunks...")
            print("This may take a while on first run...")
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            
            if vector_store_path:
                print(f"Saving vector store to {vector_store_path}")
                self.vector_store.save_local(vector_store_path)
    
    def setup_qa_chain(self) -> None:
        """Setup the QA chain using the vector store"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call build_vector_store first.")
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )
    
    def answer_question(self, question: str) -> dict:
        """
        Answer a question using RAG
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not setup. Call setup_qa_chain first.")
        
        result = self.qa_chain({
            "query": question
        })
        
        return {
            "question": question,
            "answer": result["result"],
            "sources": result.get("source_documents", [])
        }
    
    def get_relevant_documents(self, question: str, k: int = 3) -> List:
        """
        Get relevant documents for a question
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search(question, k=k)
