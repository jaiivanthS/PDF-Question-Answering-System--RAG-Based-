"""
Text Processing Module - LangChain Implementation

This module handles text chunking and processing using LangChain.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """Process and chunk text using LangChain text splitters."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize the text processor.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            separators: List of separators to use for splitting (in priority order)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len,
        )
        
        logger.info(
            f"TextProcessor initialized with chunk_size={chunk_size}, "
            f"chunk_overlap={chunk_overlap}"
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: Input text to split
            
        Returns:
            List of text chunks
        """
        try:
            logger.info(f"Splitting text of length {len(text)}")
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise
    
    def create_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Create document chunks with metadata.
        
        Args:
            texts: List of texts to process
            metadatas: Optional list of metadata dictionaries for each text
            
        Returns:
            List of dictionaries containing:
                - text: Chunk text
                - metadata: Associated metadata
        """
        try:
            all_chunks = []
            
            for i, text in enumerate(texts):
                chunks = self.split_text(text)
                metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                
                for chunk_idx, chunk in enumerate(chunks):
                    chunk_metadata = metadata.copy()
                    chunk_metadata['chunk_index'] = chunk_idx
                    chunk_metadata['total_chunks'] = len(chunks)
                    
                    all_chunks.append({
                        'text': chunk,
                        'metadata': chunk_metadata
                    })
            
            logger.info(f"Created {len(all_chunks)} document chunks from {len(texts)} texts")
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error creating documents: {str(e)}")
            raise
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        text = text.replace('\x00', '')
        
        return text
