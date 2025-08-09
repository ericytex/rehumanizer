# 📱 GitHub Setup & Deployment Guide

## 🚀 **Step 1: Create GitHub Repository**

### **Option A: GitHub Web Interface (Recommended)**
1. Go to https://github.com/new
2. **Repository name**: `rehumanizer` or `ai-humanizer`
3. **Description**: `AI text humanization system that fools all major AI detectors`
4. **Visibility**: Public (or Private if you prefer)
5. **DON'T** initialize with README (we already have one)
6. Click **"Create repository"**

### **Option B: GitHub CLI (if you have it)**
```bash
gh repo create rehumanizer --public --description "AI text humanization system"
```

---

## 🔗 **Step 2: Connect & Push to GitHub**

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/rehumanizer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌊 **Step 3: Deploy to Vercel from GitHub**

### **Automatic Deployment (Best)**
1. Go to https://vercel.com
2. Click **"New Project"**
3. **Import from GitHub**: Select your `rehumanizer` repository
4. **Framework**: Next.js (auto-detected)
5. **Root Directory**: `frontend`
6. Click **"Deploy"**

### **Environment Variables**
After deployment:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add: `GEMINI_API_KEY` = `your_gemini_api_key_here`
3. **Redeploy** (or it will work on next request)

---

## ✅ **Step 4: Test Your Live App**

Your app will be live at: `https://your-project.vercel.app`

**Test these URLs:**
- **Homepage**: `https://your-project.vercel.app`
- **Health Check**: `https://your-project.vercel.app/api/health`
- **Humanizer**: `https://your-project.vercel.app/humanize`

---

## 🔄 **Automatic Updates**

Once connected:
- **Every git push** → **Automatic Vercel deployment**
- **Pull requests** → **Preview deployments**
- **Main branch** → **Production deployment**

---

## 🎯 **Complete Commands Summary**

```bash
# 1. Create GitHub repo at https://github.com/new

# 2. Connect and push (replace USERNAME)
git remote add origin https://github.com/USERNAME/rehumanizer.git
git branch -M main
git push -u origin main

# 3. Deploy on Vercel
# Go to https://vercel.com → New Project → Import from GitHub

# 4. Add environment variables in Vercel dashboard
# GEMINI_API_KEY = your_key_here

# 5. You're LIVE! 🎉
```

---

## 🚀 **Repository Features Ready**

Your repo includes:
✅ **Complete source code**
✅ **Deployment scripts**
✅ **Documentation**
✅ **Environment setup**
✅ **Production configs**
✅ **Professional README**

**Perfect for:**
- 🌟 **GitHub showcasing**
- 👥 **Team collaboration**
- 🔄 **Continuous deployment**
- 📱 **Mobile development**
- 💼 **Portfolio projects**

---

## 🎊 **You're Ready to Go Viral!**

Once on GitHub + Vercel:
- ✅ **Professional deployment**
- ✅ **Automatic scaling**
- ✅ **Global CDN**
- ✅ **Custom domains**
- ✅ **SSL certificates**
- ✅ **99.99% uptime**

**Time to launch your AI detection evasion empire!** 🌍✨ 