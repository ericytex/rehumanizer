# 🚀 QUICK DEPLOYMENT GUIDE

## ✅ **Ready to Deploy Your Working System!**

### **🌐 Step 1: Static Frontend (Vercel)**

1. **Go to**: https://vercel.com/new
2. **Import**: `ericytex/rehumanizer`
3. **Settings**:
   ```
   Framework Preset: Other
   Root Directory: static-frontend
   Build Command: echo "Static site ready"
   Output Directory: .
   ```
4. **Deploy** → Your frontend will be live!

### **🐍 Step 2: Python Backend (Railway)**

1. **Go to**: https://railway.app/new
2. **Deploy from GitHub**: `ericytex/rehumanizer`
3. **Settings**:
   ```
   Root Directory: backend
   Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   ENVIRONMENT=production
   ```

### **🔗 Step 3: Connect Frontend to Backend**

1. **Copy your Railway URL** (e.g., `https://backend-production-abc123.railway.app`)
2. **Update the frontend**:
   - Edit `static-frontend/index.html`
   - Change `API_BASE` to your Railway URL
   - Commit and push to GitHub
   - Vercel will auto-redeploy

### **🎉 Step 4: Test Your Live App!**

- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app/health`
- **Test**: Enter AI text and watch it get humanized!

---

## 💰 **Costs**
- **Vercel**: FREE
- **Railway**: FREE for first month, then ~$5/month
- **Gemini API**: ~$5-20/month
- **Total**: ~$10-25/month

## 🚀 **Ready to Go Live?**

**Start with Step 1 (Vercel frontend) right now!** 