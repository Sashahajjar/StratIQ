# StratIQ

AI-powered business intelligence and market analysis platform.

## 🚀 Quick Deploy (No Commands Needed!)

### For Non-Technical Users

**Option 1: Vercel + Railway (Recommended)**
1. Deploy backend: [railway.app](https://railway.app) → New Project → Connect GitHub → Select `backend` folder
2. Deploy frontend: [vercel.com](https://vercel.com) → New Project → Connect GitHub → Select `frontend` folder
3. Set `NEXT_PUBLIC_API_URL` in Vercel to your Railway URL
4. Set `CORS_ORIGINS` in Railway to your Vercel URL

**See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed step-by-step instructions.**

---

## 🛠️ Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📦 Tech Stack

- **Frontend**: Next.js 15, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI**: OpenAI / Groq (free alternative)
- **Data**: Alpha Vantage, Yahoo Finance, Crunchbase

---

## 🔑 Environment Variables

See `DEPLOYMENT.md` for full list. Key ones:
- `OPENAI_API_KEY` or `GROQ_API_KEY` (for AI features)
- `RAPIDAPI_KEY` (optional, for enhanced data)
- `CORS_ORIGINS` (for production)
- `NEXT_PUBLIC_API_URL` (frontend → backend URL)

---

## 📝 License

MIT

