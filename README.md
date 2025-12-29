# Mini Chat BI

Minimalist Chat BI Tool. Upload Excel, Ask Questions, Get Insights.

## Project Structure

- `frontend/`: Vue 3 + Vite + TypeScript
- `backend/`: FastAPI + Python 3.10
- `data/`: Local storage for uploads and SQLite DB

## Quick Start

### Backend

1. Create Conda environment:
   ```bash
   conda create -n chat_bi_backend python=3.10
   conda activate chat_bi_backend
   ```
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run server (with API Key):
   ```bash
   # Replace with your actual Ark API Key
   export ARK_API_KEY="your_api_key_here"
   uvicorn app.main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run dev server:
   ```bash
   npm run dev
   ```
