# 🔥 Firebase Configuration - Final Steps

## ✅ Backend Admin SDK - DONE!
Your Firebase Admin SDK credentials are saved:
- Location: `backend/firebase-admin-key.json`
- Project: `edupath-e0735`
- Status: ✅ Ready for backend token verification

## ⚠️ Frontend Web Config - ACTION NEEDED

You need to get the **Firebase Web API configuration** for the frontend.

### Quick Steps:

1. **Go to Firebase Console**
   - Open: https://console.firebase.google.com/project/edupath-e0735/settings/general

2. **Scroll to "Your apps" section**
   - If you see a web app already, click the gear icon to view config
   - If no web app exists, click the **Web icon** (</>) to create one

3. **Get the Config Object**
   You'll see something like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "edupath-e0735.firebaseapp.com",
     projectId: "edupath-e0735",
     storageBucket: "edupath-e0735.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abc123def456"
   };
   ```

4. **Update Two Files**

   **File 1**: `frontend/config/firebase-config.json`
   ```json
   {
     "apiKey": "AIzaSy...",
     "authDomain": "edupath-e0735.firebaseapp.com",
     "projectId": "edupath-e0735",
     "storageBucket": "edupath-e0735.appspot.com",
     "messagingSenderId": "123456789012",
     "appId": "1:123456789012:web:abc123"
   }
   ```

   **File 2**: `.env` (update these lines)
   ```env
   FIREBASE_API_KEY=AIzaSy...
   FIREBASE_MESSAGING_SENDER_ID=123456789012
   FIREBASE_APP_ID=1:123456789012:web:abc123
   ```

## 🔒 Enable Authentication

While in Firebase Console:

1. **Go to Authentication**
   - Click "Authentication" in left menu
   - Click "Get started"

2. **Enable Sign-in Methods**
   - Click "Sign-in method" tab
   - Enable **Email/Password**: Toggle ON
   - Enable **Google**: Toggle ON, add support email
   - Click "Save"

## 💾 Create Firestore Database

1. **Go to Firestore Database**
   - Click "Firestore Database" in left menu
   - Click "Create database"

2. **Choose Mode**
   - Select "Start in production mode"
   - Choose closest location
   - Click "Enable"

3. **Set Security Rules**
   - Go to "Rules" tab
   - Replace with:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /users/{userId} {
         allow read, write: if request.auth != null && request.auth.uid == userId;
       }
       match /students/{studentId} {
         allow read: if request.auth != null;
         allow write: if request.auth != null && 
           get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
       }
     }
   }
   ```
   - Click "Publish"

## ✅ Verification Checklist

- [x] Backend Admin SDK saved (`backend/firebase-admin-key.json`)
- [x] Project ID updated in `.env` (`edupath-e0735`)
- [ ] Get Firebase Web config from console
- [ ] Update `frontend/config/firebase-config.json`
- [ ] Update `.env` with Web API keys
- [ ] Enable Email/Password authentication
- [ ] Enable Google authentication
- [ ] Create Firestore database
- [ ] Set Firestore security rules

## 🧪 Test After Setup

1. Restart backend: Close cmd window, run `.\START.ps1`
2. Open: `frontend/auth/signup.html`
3. Create test account
4. Should work without errors!

## 🚀 Quick Commands

```powershell
# Restart backend with new config
.\START.ps1

# Check if Firebase is connected
curl.exe http://localhost:5000/api/health
# Should show: "firebase_connected": true
```

## 📖 Need Help?

- Can't find web config? https://console.firebase.google.com/project/edupath-e0735/settings/general
- Authentication issues? Check AUTHENTICATION_GUIDE.md
- General setup? Check ENVIRONMENT_SETUP.md

---

**Current Status**: Backend Admin SDK ✅ | Frontend Web Config ⏳
