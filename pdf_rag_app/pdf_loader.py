"""
PDF Loader Module for RAG System
Handles loading and processing PDF documents
"""

from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFLoader:
    """Load and process PDF documents"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF Loader
        
        Args:
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_pdf(self, file_path: str) -> List:
        """
        Load a single PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of document chunks
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return chunks
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
            return []
    
    def load_pdfs_from_directory(self, directory_path: str) -> List:
        """
        Load all PDF files from a directory
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            List of all document chunks
        """
        all_chunks = []
        pdf_dir = Path(directory_path)
        
        if not pdf_dir.exists():
            print(f"Directory {directory_path} does not exist")
            return all_chunks
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            print(f"Loading: {pdf_file.name}")
            chunks = self.load_pdf(str(pdf_file))
            all_chunks.extend(chunks)
        
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
