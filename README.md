# PDF RAG Question-Answering System with Ollama

A fully local Retrieval-Augmented Generation (RAG) system for answering questions about PDF documents using Ollama.

## Project Structure

```
pdf_rag_app/
├── main.py              # Main application entry point
├── pdf_loader.py        # PDF loading and document chunking
├── rag.py               # RAG system implementation with Ollama
├── requirements.txt     # Python dependencies
├── data/                # Directory for PDF files to analyze
└── vector_store/        # Directory for storing vector embeddings
```

## Features

- **100% Local**: Runs completely offline using Ollama
- **PDF Loading**: Automatically loads and processes all PDFs from the `data/` directory
- **Document Chunking**: Intelligently splits documents into overlapping chunks
- **Vector Embeddings**: Uses Ollama's embeddings for semantic search
- **RAG Chain**: Combines retrieval with local LLM for accurate Q&A
- **Interactive Session**: Command-line interface for asking questions
- **Source Attribution**: Shows which documents the answers come from

## Prerequisites

### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

### 2. Pull Required Models

Open a terminal and run:

```bash
# Pull the embedding model
ollama pull nomic-embed-text

# Pull the LLM model (choose one)
ollama pull mistral
# OR
ollama pull llama2
# OR
ollama pull neural-chat
```

### 3. Start Ollama Server

In a terminal, run:

```bash
ollama serve
```

This will start Ollama on `http://localhost:11434`

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add PDF Files

Place your PDF files in the `pdf_rag_app/data/` directory:

```
pdf_rag_app/data/
├── document1.pdf
├── document2.pdf
└── ...
```

### 3. Configure Models (Optional)

Edit `pdf_rag_app/.env` to change models:

```
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=mistral
```

**Available Models:**
- **LLM Models**: llama2, mistral, neural-chat, orca-mini, zephyr
- **Embedding Models**: nomic-embed-text, all-minilm

## Usage

### 1. Start Ollama (in one terminal)

```bash
ollama serve
```

### 2. Run the Application (in another terminal)

```bash
cd pdf_rag_app
python main.py
```

### 3. Ask Questions

```
Your question: What are the main topics covered?
Your question: Summarize the key findings
Your question: exit
```

## How It Works

1. **PDF Loading**: PDFLoader reads all PDFs and splits them into chunks
2. **Embeddings**: Each chunk is converted to vector embeddings using Ollama
3. **Vector Store**: FAISS stores and indexes embeddings for fast retrieval
4. **Retrieval**: When you ask a question, the system finds the most relevant chunks
5. **Generation**: The local LLM generates an answer using the retrieved context

## Configuration

Modify parameters in `main.py`:

- `chunk_size`: Size of text chunks (default: 1000 characters)
- `chunk_overlap`: Overlap between chunks (default: 200 characters)
- `k`: Number of documents to retrieve (default: 3)
- `temperature`: Response creativity (0-1, default: 0.7)

## Model Performance

| Model | Speed | Quality | Memory |
|-------|-------|---------|--------|
| mistral | Fast | Very Good | ~8GB |
| llama2 | Medium | Excellent | ~8GB |
| neural-chat | Very Fast | Good | ~4GB |
| orca-mini | Very Fast | Fair | ~2GB |
| zephyr | Medium | Good | ~4GB |

## Troubleshooting

### Error: "Cannot connect to Ollama at http://localhost:11434"

- Make sure Ollama is running: `ollama serve`
- Check that Ollama is on port 11434
- Verify models are installed: `ollama list`

### Error: "Model not found"

Pull the required models:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### Slow Embedding Generation

- This is normal for first run
- Embeddings are cached in `vector_store/`
- Subsequent runs will be faster

### Out of Memory

- Reduce chunk_size in main.py
- Use a smaller model (orca-mini instead of mistral)
- Use all-minilm instead of nomic-embed-text for embeddings

## Dependencies

- **langchain**: RAG framework
- **ollama**: Local LLM integration
- **faiss-cpu**: Vector store
- **pypdf**: PDF loading
- **python-dotenv**: Configuration management

## Notes

- First run with embeddings will take time depending on PDF size
- All data stays local - no cloud uploads
- Internet connection not required after models are downloaded
- Respects PDF copyright - use only with authorized PDFs
