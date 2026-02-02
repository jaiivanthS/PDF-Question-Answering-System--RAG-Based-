# Data Directory

This directory contains all data files for the PDF Question Answering System.

## Structure

### `/raw/`
Store your original PDF files here. These files will be processed by the system.

**Example:**
```
data/raw/
├── research_paper_1.pdf
├── textbook_chapter_2.pdf
└── documentation.pdf
```

### `/processed/`
Contains processed and chunked documents. This directory is auto-generated during document processing.

**Note:** This directory is gitignored as processed files can be regenerated from raw PDFs.

### `/vector_stores/`
Stores the vector database files (e.g., ChromaDB, FAISS indices).

**Note:** This directory is gitignored. Vector stores can be rebuilt from raw PDFs.

## Usage

1. Place your PDF files in the `raw/` directory
2. Run the preprocessing script or use the application to process them
3. The system will automatically create embeddings and store them in `vector_stores/`

## Important Notes

- Keep your raw PDFs backed up separately
- The `processed/` and `vector_stores/` directories are regenerable
- Large PDF files may take time to process
- Ensure sufficient disk space for vector stores
