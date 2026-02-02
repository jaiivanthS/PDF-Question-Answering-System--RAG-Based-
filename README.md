# PDF Question Answering System (RAG-Based)

A powerful Retrieval-Augmented Generation (RAG) system for answering questions about PDF documents using state-of-the-art AI technologies.

## 🚀 Features

- **PDF Processing**: Extract text from PDF documents using PyMuPDF
- **Intelligent Chunking**: Smart text splitting with LangChain
- **Semantic Search**: Fast similarity search using ChromaDB vector database
- **AI-Powered Answers**: Generate accurate answers using OpenRouter API (access to multiple LLMs)
- **User-Friendly UI**: Interactive Streamlit interface
- **REST API**: FastAPI backend for programmatic access
- **Persistent Storage**: ChromaDB for efficient vector storage

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **PDF Parsing** | PyMuPDF |
| **Text Chunking** | LangChain |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector Database** | ChromaDB |
| **LLM** | OpenRouter API (supports multiple models) |

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

## 🔧 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd PDF-Question-Answering-System--RAG-Based-
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env and add your OpenRouter API key
# OPENROUTER_API_KEY=your_api_key_here
```

5. **Install the package in development mode**
```bash
pip install -e .
```

## 🎯 Usage

### Option 1: Streamlit UI (Recommended for beginners)

```bash
streamlit run src/pdf_rag/ui/streamlit_app.py
```

Then:
1. Open your browser to http://localhost:8501
2. Upload a PDF file using the sidebar
3. Click "Process PDF"
4. Ask questions about the document!

### Option 2: FastAPI Backend

```bash
# Start the API server
python -m uvicorn src.pdf_rag.api.routes:app --reload
```

API will be available at http://localhost:8000

**API Endpoints:**
- `GET /` - API status
- `POST /upload-pdf` - Upload and process PDF
- `POST /ask` - Ask a question
- `GET /documents/count` - Get document count
- `DELETE /documents/clear` - Clear all documents

**Example API Usage:**
```python
import requests

# Upload PDF
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload-pdf",
        files={"file": f}
    )

# Ask a question
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is this document about?"}
)
print(response.json()["answer"])
```

## 📁 Project Structure

```
src/pdf_rag/
├── core/              # Core RAG functionality
│   ├── pdf_loader.py      # PyMuPDF PDF loading
│   ├── embeddings.py      # Sentence Transformers embeddings
│   ├── vector_store.py    # ChromaDB vector storage
│   └── retriever.py       # RAG retrieval logic
├── models/            # LLM integration
│   ├── llm_config.py      # OpenRouter LLM
│   └── prompt_templates.py # Prompt templates
├── utils/             # Utilities
│   ├── text_processing.py # LangChain text chunking
│   └── config_loader.py   # Configuration management
├── api/               # FastAPI backend
│   └── routes.py          # API endpoints
└── ui/                # User interface
    └── streamlit_app.py   # Streamlit UI
```

## ⚙️ Configuration

Configuration files are located in the `configs/` directory:

- **`model_config.yaml`**: LLM and embedding model settings
- **`rag_config.yaml`**: RAG pipeline configuration (chunk size, retrieval settings, etc.)
- **`logging_config.yaml`**: Logging configuration

## 🔑 OpenRouter API

This project uses OpenRouter API which provides access to multiple LLM providers through a single API. 

**Free Models Available:**
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemma-2-9b-it:free`
- `mistralai/mistral-7b-instruct:free`

**Paid Models (Better Quality):**
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4-turbo`
- `google/gemini-pro-1.5`

Change the model in `configs/model_config.yaml` under `llm.model_name`.

## 🐛 Troubleshooting

**Issue: "OpenRouter API key not provided"**
- Make sure you've created a `.env` file with your API key
- Ensure the key is correctly formatted: `OPENROUTER_API_KEY=sk-or-...`

**Issue: "No module named 'pdf_rag'"**
- Run `pip install -e .` from the project root directory

**Issue: ChromaDB errors**
- Delete the `data/vector_stores` directory and restart

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using RAG technology**
