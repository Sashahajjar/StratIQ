# StratIQ Deployment Guide

This guide will help you deploy StratIQ to make it accessible online without running commands locally.

## 🚀 Quick Deployment (Recommended)

### Option 1: Vercel + Railway (Easiest)

#### Step 1: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your StratIQ repository
4. Railway will auto-detect the backend folder
5. If not, set the **Root Directory** to `backend`
6. Add environment variables in Railway dashboard:
   - `OPENAI_API_KEY` (optional, for OpenAI)
   - `GROQ_API_KEY` (optional, for free AI)
   - `RAPIDAPI_KEY` (optional, for enhanced data)
   - `CORS_ORIGINS` (set to your Vercel URL after deployment)
7. Railway will automatically deploy and give you a URL like: `https://your-app.railway.app`

#### Step 2: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "Add New Project" → Import your GitHub repository
3. Set the **Root Directory** to `frontend`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = Your Railway backend URL (e.g., `https://your-app.railway.app`)
5. Click "Deploy"
6. Vercel will give you a URL like: `https://your-app.vercel.app`

#### Step 3: Update CORS

1. Go back to Railway dashboard
2. Update `CORS_ORIGINS` environment variable to include your Vercel URL:
   ```
   https://your-app.vercel.app,https://your-app.vercel.app
   ```
3. Redeploy the backend

**Done!** Your app is now live at your Vercel URL.

---

### Option 2: Vercel + Render (Alternative)

#### Step 1: Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `stratiq-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Click "Create Web Service"
7. Render will give you a URL like: `https://your-app.onrender.com`

#### Step 2: Deploy Frontend to Vercel

Same as Option 1, Step 2, but use your Render URL for `NEXT_PUBLIC_API_URL`

---

## 📋 Environment Variables Checklist

### Backend (Railway/Render)
- `OPENAI_API_KEY` - Optional, for OpenAI AI features
- `GROQ_API_KEY` - Optional, for free Groq AI (recommended)
- `RAPIDAPI_KEY` - Optional, for enhanced market data
- `CORS_ORIGINS` - Your frontend URL(s), comma-separated
- `DATABASE_URL` - Auto-provided by Railway/Render (optional)

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL` - Your backend URL (e.g., `https://your-app.railway.app`)

---

## 🎯 One-Click Deploy (Future)

For even easier deployment, you can:
1. Use Vercel's "Deploy" button (add to README)
2. Use Railway's "Deploy" button
3. Set up GitHub Actions for automatic deployments

---

## 🔧 Troubleshooting

### CORS Errors
- Make sure `CORS_ORIGINS` in backend includes your frontend URL
- Include both `https://` and `http://` versions if needed

### API Not Working
- Check that `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Verify backend is running (check Railway/Render logs)
- Check browser console for errors

### Build Failures
- Check that all dependencies are in `requirements.txt` (backend)
- Check that all dependencies are in `package.json` (frontend)
- Review build logs in Vercel/Railway/Render dashboard

---

## 💰 Cost Estimate

- **Vercel**: Free tier (hobby) - Perfect for personal projects
- **Railway**: Free tier with $5 credit/month - Usually enough
- **Render**: Free tier available (with limitations)

**Total: $0-5/month** for most use cases!

---

## 📝 Notes

- Both platforms auto-deploy on git push
- Environment variables are managed in each platform's dashboard
- No need to run commands locally after initial setup
- Updates are automatic when you push to GitHub

