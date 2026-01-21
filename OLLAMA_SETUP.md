## Quick Start Guide - Ollama Setup

### Step 1: Download and Install Ollama
Visit https://ollama.ai and download the installer for your OS (Windows, Mac, Linux)

### Step 2: Download Required Models
Open PowerShell/Terminal and run:

```powershell
# Download the embedding model (required)
ollama pull nomic-embed-text

# Download an LLM model (choose one)
ollama pull mistral
```

These will download ~5-8GB of models, so this may take a few minutes.

### Step 3: Start Ollama Server
In PowerShell/Terminal, run:

```powershell
ollama serve
```

You should see output like:
```
started serving on 127.0.0.1:11434
```

**Leave this running!** Open a NEW terminal/PowerShell window for the next steps.

### Step 4: Install Python Dependencies
In the new terminal, run:

```powershell
cd C:\Users\jaiva\Projects\PDF-Question-Answering-System--RAG-Based-
pip install -r pdf_rag_app/requirements.txt
```

### Step 5: Add PDF Files
Copy your PDF files to:
```
C:\Users\jaiva\Projects\PDF-Question-Answering-System--RAG-Based-\pdf_rag_app\data\
```

### Step 6: Run the Application
In the same terminal, run:

```powershell
cd pdf_rag_app
python main.py
```

You should see:
```
✓ Connected to Ollama at http://localhost:11434
Initializing RAG System with Ollama...
Found X PDF files
Creating embeddings for X document chunks...
RAG System initialized successfully!

============================================================
PDF RAG Question-Answering System (Ollama)
============================================================
Enter your questions about the PDF documents.
Type 'exit' to quit.

Your question:
```

### Step 7: Ask Questions
Type your questions and press Enter:

```
Your question: What is the main topic of the document?
```

Wait for the response (first response takes longer as LLM loads).

Type `exit` to quit.

## Troubleshooting

### "Cannot connect to Ollama at http://localhost:11434"
- Check if Ollama is running in the first terminal
- Make sure you ran `ollama serve`
- Check port 11434 is accessible

### "Model not found"
- Run: `ollama pull mistral`
- Run: `ollama pull nomic-embed-text`
- Run: `ollama list` to see installed models

### First response is very slow
- This is normal - Ollama is loading the model into memory
- Subsequent responses will be faster

### Out of memory error
- Close other applications
- Use a smaller model: `ollama pull orca-mini` and update .env
- Reduce chunk_size in main.py

## Alternative Models

If mistral is too slow, try:

```powershell
# Fast & good quality
ollama pull neural-chat

# Very fast & lightweight
ollama pull orca-mini

# High quality but slower
ollama pull llama2
```

Then update `.env`:
```
LLM_MODEL=neural-chat
```

## Next Steps

- Add more PDFs to the `data/` folder
- Experiment with different models
- Adjust `chunk_size` and `chunk_overlap` in main.py for better results
- Change `temperature` for more/less creative responses
