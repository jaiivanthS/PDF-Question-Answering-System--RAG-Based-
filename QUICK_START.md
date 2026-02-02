# Quick Start Guide

## ✅ Fixes Applied

### Issue 1: OpenRouter API Key Not Loading
**Fixed:** Moved `load_dotenv()` to the very top of `streamlit_app.py` before any other imports to ensure environment variables are loaded first.

### Issue 2: PyTorch Meta Tensor Error
**Fixed:** Upgraded packages to compatible versions:
- `sentence-transformers`: 2.3.1 → 2.7.0
- `torch`: Added explicit version 2.2.0

## 🚀 How to Run

### Step 1: Stop Current Streamlit Instance
In your terminal, press `Ctrl+C` to stop the currently running Streamlit app.

### Step 2: Restart Streamlit
```bash
streamlit run src/pdf_rag/ui/streamlit_app.py
```

### Step 3: Verify It Works
1. Open http://localhost:8501 in your browser
2. You should see "PDF Question Answering System" without errors
3. The embedding model should load successfully

## 🧪 Test the System

1. **Upload a PDF**:
   - Click "Browse files" in the sidebar
   - Select any PDF document
   - Click "Process PDF"

2. **Ask a Question**:
   - Type a question in the text box
   - Click "Get Answer"
   - View the AI-generated answer and source documents

## 🔍 Troubleshooting

### If you still see "OpenRouter API key not provided":
1. Check that `.env` file exists in the project root
2. Verify it contains: `OPENROUTER_API_KEY=sk-or-v1-...`
3. Restart Streamlit completely

### If you see PyTorch errors:
The packages have been upgraded. If issues persist:
```bash
pip uninstall torch sentence-transformers -y
pip install torch==2.2.0 sentence-transformers==2.7.0
```

## 📝 Your API Key
Your OpenRouter API key is safely stored in `.env`:
```
OPENROUTER_API_KEY=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
```

**Security Note:** This file is in `.gitignore` and won't be committed to Git. ✅

## 🎯 Next Steps
Once Streamlit loads successfully:
1. Upload a PDF document
2. Process it (this will take a minute for the first time)
3. Ask questions about the content
4. Enjoy your RAG system! 🎉
