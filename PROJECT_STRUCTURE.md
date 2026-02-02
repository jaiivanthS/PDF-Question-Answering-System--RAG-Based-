# PDF Question Answering System - Project Structure

## Directory Layout

```
PDF-Question-Answering-System--RAG-Based-/
│
├── src/                          # Source code
│   └── pdf_rag/                  # Main application package
│       ├── __init__.py
│       ├── core/                 # Core RAG functionality
│       │   ├── __init__.py
│       │   ├── pdf_loader.py     # PDF loading and parsing
│       │   ├── embeddings.py     # Text embedding generation
│       │   ├── vector_store.py   # Vector database operations
│       │   └── retriever.py      # Document retrieval logic
│       │
│       ├── models/               # LLM and model configurations
│       │   ├── __init__.py
│       │   ├── llm_config.py     # LLM setup (OpenRouter API)
│       │   └── prompt_templates.py # Prompt engineering templates
│       │
│       ├── utils/                # Utility functions
│       │   ├── __init__.py
│       │   ├── text_processing.py # Text chunking with LangChain
│       │   ├── config_loader.py   # Configuration management
│       │   └── logger.py          # Logging utilities
│       │
│       ├── api/                  # API endpoints (FastAPI)
│       │   ├── __init__.py
│       │   ├── routes.py         # API route definitions
│       │   └── schemas.py        # Pydantic models/schemas
│       │
│       └── ui/                   # User interface
│           ├── __init__.py
│           └── streamlit_app.py  # Streamlit UI
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/                     # Unit tests
│   │   ├── __init__.py
│   │   ├── test_pdf_loader.py
│   │   ├── test_embeddings.py
│   │   └── test_retriever.py
│   │
│   └── integration/              # Integration tests
│       ├── __init__.py
│       └── test_rag_pipeline.py
│
├── data/                         # Data directory
│   ├── raw/                      # Original PDF files
│   ├── processed/                # Processed/chunked documents
│   └── vector_stores/            # Vector database storage
│
├── configs/                      # Configuration files
│   ├── model_config.yaml         # Model configurations
│   ├── rag_config.yaml           # RAG pipeline settings
│   └── logging_config.yaml       # Logging configuration
│
├── notebooks/                    # Jupyter notebooks
│   ├── exploration.ipynb         # Data exploration
│   └── experiments.ipynb         # Model experiments
│
├── scripts/                      # Utility scripts
│   ├── setup_env.py              # Environment setup script
│   └── preprocess_pdfs.py        # Batch PDF preprocessing
│
├── logs/                         # Application logs
│
├── docs/                         # Documentation
│   ├── architecture.md           # System architecture
│   ├── api_reference.md          # API documentation
│   └── user_guide.md             # User guide
│
├── pdf_rag_app/                  # Legacy code (to be migrated)
│
├── .env                          # Environment variables
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
├── pyproject.toml                # Modern Python project config
└── README.md                     # Project README
```

## Directory Descriptions

### `/src/pdf_rag/`
Main application package containing all source code.

- **core/**: Core RAG functionality including PDF loading (PyMuPDF), embeddings (Sentence Transformers), vector storage (ChromaDB), and retrieval
- **models/**: LLM configurations (OpenRouter API) and prompt templates
- **utils/**: Shared utility functions for text processing (LangChain), configuration, and logging
- **api/**: REST API implementation using FastAPI
- **ui/**: User interface using Streamlit

### `/tests/`
Comprehensive test suite with unit and integration tests.

### `/data/`
Data storage organized by processing stage:
- **raw/**: Original uploaded PDFs
- **processed/**: Chunked and processed documents (LangChain)
- **vector_stores/**: Persistent ChromaDB vector database files

### `/configs/`
YAML configuration files for models, RAG pipeline, and logging.

### `/notebooks/`
Jupyter notebooks for experimentation and exploration.

### `/scripts/`
Standalone scripts for setup, preprocessing, and maintenance tasks.

### `/logs/`
Application logs (gitignored).

### `/docs/`
Project documentation including architecture, API reference, and user guides.

## Migration Plan

The existing `pdf_rag_app/` directory contains legacy code that should be migrated to the new structure:
- `main.py` → `src/pdf_rag/ui/streamlit_app.py` or `src/pdf_rag/api/routes.py`
- `pdf_loader.py` → `src/pdf_rag/core/pdf_loader.py`
- `rag.py` → Split into `src/pdf_rag/core/` modules
- `data/` → `data/raw/`
- `vector_store/` → `data/vector_stores/`

## Best Practices

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Testability**: Clear separation enables comprehensive testing
3. **Scalability**: Modular structure supports growth and feature additions
4. **Configuration Management**: Externalized configs for easy deployment
5. **Documentation**: Comprehensive docs for maintainability
