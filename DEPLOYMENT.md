# 🚀 ClaritFi AI — Deployment Guide

This guide provides step-by-step instructions to deploy **ClaritFi AI** to production using free & easy hosting platforms.

---

## 🏗️ Architecture Overview

- **Backend**: Python FastAPI (`/backend`) → Deployed on **Render** (or Railway / Fly.io)
- **Frontend**: Next.js 15 (`/frontend`) → Deployed on **Vercel**

---

## Step 1: Deploy Backend (FastAPI on Render.com)

1. Push your project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for ClaritFi AI"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/claritfi-ai.git
   git push -u origin main
   ```

2. Go to [Render.com](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Configure the settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Add Environment Variables under **Environment**:
   - `GEMINI_API_KEY`: `your_actual_google_gemini_api_key`
6. Click **Deploy Web Service**.
7. Copy your backend live URL (e.g., `https://claritfi-backend.onrender.com`).

---

## Step 2: Deploy Frontend (Next.js on Vercel)

1. Go to [Vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New...** → **Project** and import your repository.
3. Configure project settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: Select `frontend`
4. Expand **Environment Variables** and add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://claritfi-backend.onrender.com` *(Replace with your Render backend URL)*
5. Click **Deploy**.

---

## Step 3: Test & Verify

1. Open your live Vercel URL (e.g., `https://claritfi.vercel.app`).
2. Click **Use Sample Agreement** or paste loan agreement text.
3. Click **Analyze Agreement** to confirm AI analysis, Real APR calculations, and chatbot Q&A are connecting seamlessly to your live backend.

---

## 🔒 Security Best Practices

- Never commit your `GEMINI_API_KEY` to public repositories.
- Keep `backend/.env` and `frontend/.env.local` inside `.gitignore`.
