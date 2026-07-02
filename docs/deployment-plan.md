# Deployment Plan

This document outlines the step-by-step process for deploying the **Zero-Advice Fund RAG** project. The backend will be hosted on **Railway**, which is excellent for containerized Python applications with persistent disk access (for ChromaDB). The frontend will be hosted on **Vercel**, which is optimized for Vite/React applications.

---

## 1. Backend Deployment (Railway)

Railway will host the FastAPI backend. It will read the committed `vectorstore` directly from the repository, and the GitHub Actions cron will continue to keep the repository updated.

### Setup Steps
1. **Create Project**: Log in to [Railway](https://railway.app/) and click **New Project** → **Deploy from GitHub repo**.
2. **Select Repository**: Choose your `zero-advice-fund-rag` repository.
3. **Configure Settings**: Once the service is created, go to the **Settings** tab.
4. **Environment Variables**: Go to the **Variables** tab and add:
   - `GROQ_API_KEY`: `<your_groq_api_key>`
5. **Build & Start Commands**: Go to the **Settings** tab and configure the Nixpacks build:
   - **Root Directory**: Leave as `/` (Project Root).
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
6. **Deploy**: Railway will automatically build and deploy. Wait for it to finish and assign a public URL (e.g., `https://your-backend-app.up.railway.app`).
7. **Verify**: Open `https://your-backend-app.up.railway.app/api/health` in your browser. It should return `{"status":"ok"}`.

*Save this Railway URL, as you will need it for the frontend deployment.*

---

## 2. Frontend Deployment (Vercel)

Vercel will host the React frontend. Since Vercel runs on a different domain than Railway, we need to use Vercel's rewrite functionality to route `/api/*` requests to your Railway backend without changing the frontend code.

### Step 2.1: Add `vercel.json` (Required before deployment)
Before deploying to Vercel, you should add a `vercel.json` file inside the `frontend/` directory to configure the API proxy. This ensures `fetch('/api/query')` gets routed to Railway.

Create `frontend/vercel.json` with the following content:
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://<YOUR_RAILWAY_URL>/api/$1"
    }
  ]
}
```
*Note: Replace `<YOUR_RAILWAY_URL>` with your actual Railway backend URL before committing.*

Commit and push this file to your `main` branch.

### Step 2.2: Vercel Setup
1. **Create Project**: Log in to [Vercel](https://vercel.com/) and click **Add New** → **Project**.
2. **Import Repository**: Import your `zero-advice-fund-rag` repository.
3. **Configure Project**:
   - **Framework Preset**: Vercel will auto-detect **Vite**.
   - **Root Directory**: Click "Edit" and select `frontend`.
   - **Build Command**: Leave as default (`npm run build`).
   - **Output Directory**: Leave as default (`dist`).
4. **Deploy**: Click **Deploy**. Vercel will build and host the frontend.

---

## 3. GitHub Actions CI/CD (Scheduler)

Your GitHub Actions workflow (`daily-ingestion.yml`) is currently configured to run on GitHub's infrastructure, update the `backend/vectorstore`, and commit it back to the `main` branch.

**How this integrates with Deployment:**
1. Every day at 10:30 AM IST, the GitHub Action runs.
2. It scrapes new data and updates the ChromaDB vectorstore.
3. It commits the updated vectorstore to the `main` branch.
4. **Railway Auto-Deploy**: Railway automatically listens to pushes on the `main` branch. When GitHub Actions pushes the new commit, Railway will automatically trigger a new deployment, pulling in the fresh vectorstore data.
5. Zero downtime is achieved as Railway builds the new container before swapping traffic.

No changes are needed to the GitHub Actions workflow!

---

## Summary Checklist

- [ ] Backend: Deploy repo on Railway.
- [ ] Backend: Set `GROQ_API_KEY` in Railway Variables.
- [ ] Backend: Set Build/Start commands in Railway Settings.
- [ ] Backend: Copy the generated Railway public domain.
- [ ] Frontend: Create `frontend/vercel.json` using the Railway domain.
- [ ] Frontend: Commit and push `vercel.json`.
- [ ] Frontend: Import project in Vercel.
- [ ] Frontend: Set Root Directory to `frontend`.
- [ ] Frontend: Deploy on Vercel.
- [ ] Final: Open Vercel URL and test a query!
