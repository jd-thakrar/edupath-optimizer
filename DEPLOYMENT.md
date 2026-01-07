# EduPath Optimizer - Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Free Tier)

**Why Render?**
- Free tier for full-stack apps
- Automatic HTTPS
- Easy environment variables
- Good for Flask + Static frontend

**Steps:**
1. Push code to GitHub (if not already)
2. Go to [render.com](https://render.com)
3. Create new **Web Service**
4. Connect your GitHub repo
5. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt && python backend/train_model.py`
   - **Start Command:** `cd backend && python app.py`
   - **Environment:** `Python 3.10`
6. Add Environment Variables:
   - Copy all from `.env` file
   - Set `FLASK_ENV=production`
   - Set `PORT=10000` (Render default)
7. Click **Create Web Service**
8. Wait 3-5 minutes for build
9. Your live link: `https://edupath-optimizer.onrender.com`

**Serve Frontend:**
Render auto-serves static files from `frontend/` directory!

---

### Option 2: Railway (Fast & Easy)

1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub**
3. Select your repo
4. Railway auto-detects Flask
5. Add environment variables from `.env`
6. Set Root Directory: `backend`
7. Deploy! (2-3 minutes)
8. Get your URL: `https://edupath-optimizer-production.up.railway.app`

---

### Option 3: Azure (Full Control)

**Backend (Azure App Service):**
```powershell
# Login to Azure
az login

# Create resource group
az group create --name EduPathRG --location eastus

# Create App Service plan
az appservice plan create --name EduPathPlan --resource-group EduPathRG --sku F1 --is-linux

# Create web app
az webapp create --resource-group EduPathRG --plan EduPathPlan --name edupath-optimizer --runtime "PYTHON:3.10"

# Deploy code
cd backend
az webapp up --name edupath-optimizer --resource-group EduPathRG

# Configure environment variables
az webapp config appsettings set --resource-group EduPathRG --name edupath-optimizer --settings @appsettings.json
```

**Frontend (Azure Static Web Apps):**
```powershell
# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Deploy frontend
cd frontend
swa deploy --app-name edupath-frontend --resource-group EduPathRG
```

Your live link: `https://edupath-optimizer.azurewebsites.net`

---

### Option 4: Heroku (Classic)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create edupath-optimizer

# Add Python buildpack
heroku buildpacks:set heroku/python

# Push code
git push heroku main

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set FIREBASE_PROJECT_ID=edupath-e0735
# ... copy all from .env

# Open app
heroku open
```

---

### Option 5: Google Cloud Run (Containerized)

```bash
# Build Docker image
docker build -t edupath-optimizer .

# Tag for GCR
docker tag edupath-optimizer gcr.io/YOUR_PROJECT_ID/edupath-optimizer

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/edupath-optimizer

# Deploy to Cloud Run
gcloud run deploy edupath-optimizer \
  --image gcr.io/YOUR_PROJECT_ID/edupath-optimizer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production
```

---

## 📋 Pre-Deployment Checklist

### 1. Security
- [ ] Generate secure `FLASK_SECRET_KEY`
  ```powershell
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] Update `.env`: Set `FLASK_DEBUG=False`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure `CORS_ORIGINS` with your domain
- [ ] Enable `RATE_LIMITING=True`

### 2. Firebase
- [ ] Firebase Admin SDK key added to platform secrets
- [ ] Firebase Console: Enable Email/Password auth
- [ ] Firebase Console: Enable Google Sign-in
- [ ] Firestore database created
- [ ] Security rules published

### 3. Files
- [ ] `.gitignore` includes all secrets
- [ ] `requirements.txt` has all dependencies
- [ ] `Dockerfile` (if using containers)
- [ ] Environment variables configured on platform

### 4. Testing
- [ ] Backend health check: `/api/health`
- [ ] Test student risk assessment endpoint
- [ ] Test Firebase authentication
- [ ] Test file serving (frontend loads)

---

## 🌐 Platform Comparison

| Platform | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Render** | ✅ Yes | 5 min | Full-stack, easy start |
| **Railway** | ✅ Limited | 2 min | Fastest deployment |
| **Azure** | ⚠️ Trial | 10 min | Enterprise, scalability |
| **Heroku** | ✅ Yes | 5 min | Classic, reliable |
| **GCP Cloud Run** | ✅ Yes | 15 min | Containerized apps |
| **Vercel** | ✅ Yes | 3 min | Frontend + API |

---

## 🔧 Quick Deploy Commands

### Deploy to Render (Recommended)
```powershell
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to render.com and connect GitHub
# 3. Follow on-screen wizard
# Done! Get your link
```

### Deploy to Railway
```powershell
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Deploy
railway up

# 5. Get URL
railway open
```

---

## 🧪 Post-Deployment Testing

```powershell
# Replace with your actual URL
$URL = "https://your-app.onrender.com"

# Test health endpoint
curl.exe $URL/api/health

# Test risk assessment
curl.exe -X POST $URL/api/student/risk-assessment -H "Content-Type: application/json" -d '{\"random\": true}'

# Open frontend
start $URL/frontend/auth/login.html
```

---

## 🆘 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Ensure Python version matches (3.10+)
- Verify `train_model.py` runs successfully

### Backend 500 Error
- Check logs on platform dashboard
- Verify environment variables are set
- Check Firebase Admin SDK key is uploaded

### Frontend Won't Load
- Verify static file serving is enabled
- Check CORS settings in backend
- Ensure frontend files are in correct directory

### Firebase Auth Not Working
- Verify Firebase config in frontend files
- Check Firebase Console auth methods are enabled
- Verify domain is added to authorized domains

---

## 📖 Next Steps After Deployment

1. **Custom Domain:** Add your own domain in platform settings
2. **SSL Certificate:** Platform auto-generates (free)
3. **Monitoring:** Enable platform monitoring/logging
4. **CI/CD:** Set up auto-deploy on GitHub push
5. **Scaling:** Configure auto-scaling rules
6. **Backups:** Set up database backup schedule

---

## 💡 Pro Tips

1. **Use Render for simplicity** - Best free tier, easiest setup
2. **Railway for speed** - Fastest deployment, great DX
3. **Azure for production** - Best for enterprise/scaling
4. **Always test locally first** - Run `.\START.ps1` before deploying
5. **Monitor logs** - Check platform logs for errors
6. **Enable auto-deploy** - Push to GitHub → Auto deploys

---

## 🎯 Recommended: Deploy to Render Now!

```powershell
# Step 1: Push to GitHub (if not already)
git add .
git commit -m "Production ready"
git push origin main

# Step 2: Go to render.com
start https://render.com/

# Step 3: Follow the wizard
# - New Web Service
# - Connect GitHub repo
# - Build: pip install -r backend/requirements.txt && python backend/train_model.py
# - Start: cd backend && python app.py
# - Add environment variables from .env

# Step 4: Deploy! (3-5 minutes)

# Step 5: Get your link and share it! 🎉
```

---

**Your app will be live at:** `https://edupath-optimizer.onrender.com`
**Time to deploy:** 10 minutes
**Cost:** Free! 🎉
