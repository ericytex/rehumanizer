# 🎨 **RENDER DEPLOYMENT GUIDE** (100% FREE!)

## 🆓 **Why Render is Perfect for Your Backend:**

✅ **Completely FREE** - No credit card required  
✅ **Python FastAPI support** - Built for your stack  
✅ **Auto-deploy from GitHub** - Connect once, deploy forever  
✅ **512MB RAM + shared CPU** - Perfect for your API  
✅ **Automatic HTTPS** - SSL certificates included  
✅ **Environment variables** - Secure API key storage  

---

## 🚀 **Step-by-Step Render Deployment**

### **1. Backend Deployment (5 minutes)**

#### **Go to Render Dashboard**
Visit: [https://dashboard.render.com/](https://dashboard.render.com/)

#### **Create Web Service**
1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub** (if not already connected)
3. **Find Repository**: `ericytex/rehumanizer`
4. Click **"Connect"**

#### **Configure Service**
```
Name: rehumanizer-api
Environment: Python 3
Region: Oregon (US West) or Virginia (US East)
Branch: main
Root Directory: backend
```

#### **Build & Start Commands**
```
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### **Environment Variables**
Add these in the "Environment" section:
```
GEMINI_API_KEY = your_gemini_api_key_here
ENVIRONMENT = production
PORT = 10000
CORS_ORIGINS = https://your-frontend.vercel.app
```

#### **Deploy**
Click **"Create Web Service"** → Render will start building!

---

## 🌐 **Frontend Deployment (Vercel)**

### **Deploy Static Frontend**

#### **Go to Vercel**
Visit: https://vercel.com/new

#### **Import Project**
1. **Import Git Repository** → **GitHub** → `ericytex/rehumanizer`
2. **Configure Project**:
   ```
   Framework Preset: Other
   Root Directory: static-frontend
   Build Command: echo "Static site ready"
   Output Directory: .
   Install Command: echo "No install needed"
   ```
3. Click **"Deploy"**

---

## 🔗 **Connect Frontend to Backend**

### **Update API URL**

After Render gives you a URL (like `https://rehumanizer-api.onrender.com`):

1. **Edit** `static-frontend/index.html`
2. **Update** the `API_BASE` line:
   ```javascript
   const API_BASE = 'https://your-actual-render-url.onrender.com';
   ```
3. **Commit and push** to GitHub
4. **Vercel auto-redeploys** with new URL

---

## 🎯 **Complete Deployment URLs**

### **Your Live App:**
- **Frontend**: `https://rehumanizer.vercel.app`
- **Backend**: `https://rehumanizer-api.onrender.com`
- **Health Check**: `https://rehumanizer-api.onrender.com/health`
- **API Docs**: `https://rehumanizer-api.onrender.com/docs`

---

## ⚙️ **Render Service Settings**

### **Recommended Configuration:**
```
Name: rehumanizer-api
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: backend
Auto-Deploy: Yes
```

### **Advanced Settings:**
```
Python Version: 3.9 (default)
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

### **Environment Variables:**
```
GEMINI_API_KEY = your_gemini_api_key_here
ENVIRONMENT = production
PORT = 10000
CORS_ORIGINS = https://your-frontend.vercel.app,https://rehumanizer.vercel.app
```

---

## 🔄 **Render Free Tier Details**

### **What You Get FREE:**
- **512MB RAM**
- **Shared CPU**
- **750 hours/month** (25 hours/day)
- **100GB bandwidth**
- **Automatic HTTPS**
- **Custom domains**
- **Auto-deploy from GitHub**

### **Sleep Behavior:**
- **Sleeps after 15 minutes** of inactivity
- **Wakes up in ~30 seconds** on first request
- Perfect for development and low-traffic apps

### **When You'll Need to Upgrade:**
- High traffic (24/7 uptime needed)
- More than 750 hours/month usage
- Need guaranteed response times

---

## 🚨 **Important Setup Notes**

### **CORS Configuration**
Make sure your `backend/app/main.py` includes your Vercel domain:
```python
origins = [
    "https://your-app.vercel.app",
    "https://rehumanizer.vercel.app",
    "http://localhost:3000",  # For development
]
```

### **Environment Variables**
- Add your **Gemini API key** in Render dashboard
- Set **ENVIRONMENT=production**
- Include **CORS_ORIGINS** with your frontend URL

### **Health Check**
- Render will ping `/health` to check if your app is running
- Your FastAPI app already has this endpoint

---

## 🎊 **Deployment Checklist**

### **Backend (Render):**
- [ ] Create Web Service from GitHub
- [ ] Set Root Directory to `backend`
- [ ] Configure build/start commands
- [ ] Add environment variables
- [ ] Deploy and get URL

### **Frontend (Vercel):**
- [ ] Import from GitHub
- [ ] Set Root Directory to `static-frontend`
- [ ] Deploy static site
- [ ] Update API_BASE with Render URL
- [ ] Redeploy

### **Testing:**
- [ ] Visit frontend URL
- [ ] Test text humanization
- [ ] Check browser console for errors
- [ ] Verify API responses

---

## 💰 **Total Cost: 100% FREE!**

- **Render Backend**: $0/month (free tier)
- **Vercel Frontend**: $0/month (hobby plan)
- **Gemini API**: ~$5-20/month (only real cost)
- **Total**: ~$5-20/month

---

## 🚀 **Ready to Deploy?**

**Start here:** [https://dashboard.render.com/](https://dashboard.render.com/)

1. **Create Web Service** from your GitHub repo
2. **Configure** with settings above  
3. **Add environment variables**
4. **Deploy** and get your URL!
5. **Update frontend** with new URL
6. **Go live!** 🎉

**Your revolutionary AI humanization system will be live in under 10 minutes!** ✨ 