# 🏦 ClaritFi AI — Understand Before You Sign

**ClaritFi AI** is an AI-powered financial audit tool designed to protect borrowers from predatory hidden fees, confusing loan terms, and misleading interest rates.

It parses loan contracts and credit agreement documents, calculates the **Real Effective APR (Annual Percentage Rate)** using exact cash-flow internal rate of return algorithms, flags high-risk clauses, verifies grounding against source text, and translates dense legalese into plain English.

---

## ✨ Features

- 📊 **Real APR Calculation**: Solves exact Internal Rate of Return (IRR) cash flows to reveal true borrowing costs.
- 🔍 **Jargon-Free Breakdown**: Simplifies complex terms like "Foreclosure Penalty" to "Early Closing Fee".
- ⚠️ **Risk & Hidden Fee Detector**: Identifies upfront deductions, recurring account charges, and penal rates.
- 🛡️ **Verbatim Clause Grounding**: Substring grounding verification to prevent AI hallucination.
- 💬 **Interactive Contract Chatbot**: Ask questions directly about your agreement in simple language.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 15 (App Router), React, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.11, FastAPI, Pydantic v2, pdfplumber
- **AI / LLM**: Google Gemini (`gemini-2.5-flash`) via `google-generativeai`

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the FastAPI backend:
```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local` inside `frontend/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the development server:
```bash
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 📖 Deployment

Refer to [DEPLOYMENT.md](DEPLOYMENT.md) for full instructions on deploying the backend to **Render** and frontend to **Vercel**.

---

## 📄 License

MIT License © 2026 ClaritFi AI
