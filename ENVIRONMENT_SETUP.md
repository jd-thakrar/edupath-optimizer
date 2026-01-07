# 🔧 Environment Variables Setup Guide

## 📁 Files Overview

### `.env` (Active Configuration)
- **Location**: Root directory (`C:\Users\JEET\Downloads\EDU\.env`)
- **Purpose**: Active environment variables used by the application
- **Status**: ✅ Created with working defaults
- **Security**: 🚨 NEVER commit to Git (protected by .gitignore)

### `.env.example` (Template)
- **Location**: Root directory (`C:\Users\JEET\Downloads\EDU\.env.example`)
- **Purpose**: Template with all possible variables documented
- **Status**: ✅ Comprehensive template with comments
- **Security**: ✅ Safe to commit (no real credentials)

## 🚀 Quick Start

Your `.env` file is ready with defaults that work immediately:
- ✅ Flask runs on port 5000
- ✅ Demo mode enabled (no Firebase required)
- ✅ Sample student data loaded
- ✅ ML models configured
- ✅ Development settings active

**Just run `.\START.ps1` - everything works!**

## 🔑 Important Variables to Update

### 1. Firebase Configuration (Optional)
After creating your Firebase project, update these in `.env`:

```env
FIREBASE_PROJECT_ID=your-actual-project-id
FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789012
FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

**Also update**: `frontend/config/firebase-config.json` with same values

### 2. Firebase Admin SDK (Optional)
For backend token verification:

```env
FIREBASE_CREDENTIALS_PATH=backend/firebase-admin-key.json
```

Download the JSON key from Firebase Console → Project Settings → Service Accounts

### 3. Gemini API Key (Optional)
For enhanced AI explanations:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get from: https://makersuite.google.com/app/apikey

### 4. Production Security Keys
Before deploying to production, generate secure keys:

```bash
# Generate FLASK_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

Update in `.env`:
```env
FLASK_SECRET_KEY=<generated_64_char_hex>
JWT_SECRET_KEY=<generated_64_char_hex>
```

## 📋 All Environment Variables

### 🖥️ Flask Application
| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode (development/production) |
| `PORT` | `5000` | Server port |
| `FLASK_SECRET_KEY` | `dev-secret-key...` | Flask session encryption key |
| `FLASK_DEBUG` | `True` | Enable debug mode |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

### 🔥 Firebase
| Variable | Required | Description |
|----------|----------|-------------|
| `FIREBASE_PROJECT_ID` | ⚠️ Optional | Firebase project identifier |
| `FIREBASE_API_KEY` | ⚠️ Optional | Firebase Web API key |
| `FIREBASE_AUTH_DOMAIN` | ⚠️ Optional | Firebase auth domain |
| `FIREBASE_STORAGE_BUCKET` | ⚠️ Optional | Firebase storage bucket |
| `FIREBASE_MESSAGING_SENDER_ID` | ⚠️ Optional | FCM sender ID |
| `FIREBASE_APP_ID` | ⚠️ Optional | Firebase app identifier |
| `FIREBASE_CREDENTIALS_PATH` | ⚠️ Optional | Path to admin SDK JSON |

### 🤖 AI & Machine Learning
| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | `your_gemini_api_key_here` | Google Gemini API key |
| `ML_MODEL_PATH` | `ml_models/risk_predictor.pkl` | Trained ML model path |
| `FEATURE_SCALER_PATH` | `ml_models/feature_scaler.pkl` | Feature scaler path |

### 💾 Database
| Variable | Default | Description |
|----------|---------|-------------|
| `SAMPLE_STUDENTS_PATH` | `data/sample_students.json` | Sample student data |

### 🔒 Security
| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET_KEY` | `dev-jwt-secret...` | JWT token signing key |
| `TOKEN_EXPIRATION` | `3600` | Token expiry (seconds) |
| `ALLOW_DEMO_MODE` | `True` | Enable demo without auth |
| `RATE_LIMIT_PER_MINUTE` | `100` | API rate limiting |
| `ENABLE_RATE_LIMITING` | `False` | Enable rate limiting |

### 📊 Logging & Monitoring
| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `logs/app.log` | Log file path |
| `ENABLE_ERROR_TRACKING` | `True` | Track errors |

### 🌐 Frontend
| Variable | Default | Description |
|----------|---------|-------------|
| `FRONTEND_URL` | `http://localhost:5000` | Frontend base URL |
| `API_BASE_URL` | `http://localhost:5000/api` | API endpoint base |

### 🔧 Development
| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_AUTO_RELOAD` | `True` | Auto-reload on changes |
| `SQLALCHEMY_ECHO` | `False` | Log SQL queries |
| `ENABLE_PROFILER` | `False` | Enable performance profiler |

## 🔄 Environment Loading

### How Variables are Loaded:

1. **Backend** (`backend/app.py`):
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env from project root

firebase_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
port = int(os.getenv('PORT', 5000))
```

2. **Frontend** (`frontend/auth/login.html`):
```javascript
// Loads from frontend/config/firebase-config.json
const configResponse = await fetch('/config/firebase-config.json');
const firebaseConfig = await configResponse.json();
```

## 📝 Usage Examples

### Check Current Environment
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Environment: {os.getenv('FLASK_ENV')}")
print(f"Port: {os.getenv('PORT')}")
print(f"Demo Mode: {os.getenv('ALLOW_DEMO_MODE')}")
```

### Override in Code
```python
# Use environment variable with fallback
api_key = os.getenv('GEMINI_API_KEY', 'default_key')
```

### Pass to Frontend
Create `frontend/config/env.js`:
```javascript
window.ENV = {
  API_BASE_URL: 'http://localhost:5000/api',
  ENABLE_ANALYTICS: false
};
```

## 🚨 Security Best Practices

### ✅ DO:
- Use `.env` for local development
- Keep `.env` in `.gitignore`
- Use different values for development/production
- Generate strong random keys for production
- Rotate credentials regularly
- Use environment variables in hosting platforms

### ❌ DON'T:
- Commit `.env` to Git
- Share credentials in chat/email
- Use production credentials in development
- Hardcode sensitive values in code
- Use weak/default keys in production
- Store credentials in frontend code

## 🎯 Environment-Specific Configurations

### Development (Current)
```env
FLASK_ENV=development
FLASK_DEBUG=True
ALLOW_DEMO_MODE=True
CORS_ORIGINS=*
LOG_LEVEL=DEBUG
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
ALLOW_DEMO_MODE=False
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
ENABLE_RATE_LIMITING=True
```

### Testing
```env
TESTING=True
FLASK_ENV=testing
DATABASE_URL=sqlite:///test_edupath.db
```

## 🔧 Troubleshooting

### Variables Not Loading
```bash
# Check if .env exists
ls .env

# Verify python-dotenv is installed
pip install python-dotenv

# Load manually in Python
from dotenv import load_dotenv
load_dotenv(verbose=True)  # Shows what's loaded
```

### Firebase Not Working
```bash
# Check Firebase credentials
echo $FIREBASE_PROJECT_ID

# Verify JSON key exists
ls backend/firebase-admin-key.json

# Test Firebase connection
python -c "import firebase_admin; print('Firebase Admin installed')"
```

### Port Already in Use
```env
# Change port in .env
PORT=8000
```

## 📦 Deployment Platforms

### Heroku
Set variables in dashboard or CLI:
```bash
heroku config:set FLASK_ENV=production
heroku config:set FIREBASE_PROJECT_ID=your-project-id
```

### Azure
Use Application Settings in Azure Portal or:
```bash
az webapp config appsettings set --settings FLASK_ENV=production
```

### Google Cloud Run
Use environment variables in Cloud Run configuration:
```bash
gcloud run deploy --set-env-vars FLASK_ENV=production,PORT=8080
```

### Docker
Pass via docker-compose.yml:
```yaml
environment:
  - FLASK_ENV=production
  - PORT=5000
env_file:
  - .env
```

## ✅ Verification Checklist

- [x] `.env` file created
- [x] `.env.example` documented
- [x] `.gitignore` protects `.env`
- [x] Backend loads variables correctly
- [ ] Firebase credentials configured (optional)
- [ ] Gemini API key added (optional)
- [ ] Production keys generated (before deploy)
- [ ] Frontend config updated (if using Firebase)

## 🎉 You're All Set!

Your environment is configured and ready to use. The system works immediately with current settings. Update Firebase/Gemini keys only when you're ready to enable those features.

**Next Steps:**
1. Run `.\START.ps1` to start the application
2. Optionally configure Firebase (see AUTHENTICATION_GUIDE.md)
3. Optionally add Gemini API key for enhanced AI features
4. Generate production keys before deploying live

---

**Need Help?** Check other guides:
- `AUTHENTICATION_GUIDE.md` - Firebase setup
- `README.md` - General project documentation
- `DYNAMIC_FEATURES.md` - System capabilities
