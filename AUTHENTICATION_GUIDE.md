# 🔐 Firebase Authentication - Complete Setup

## ✅ What's Already Implemented

### Frontend (login.html + signup.html)
- ✅ Email/Password authentication
- ✅ Google Sign-In integration
- ✅ User registration with profile creation
- ✅ Role-based access (Student/Admin)
- ✅ Token management (stored in localStorage)
- ✅ Automatic redirect based on user role
- ✅ Demo mode fallback if Firebase not configured

### Backend (app.py)
- ✅ Firebase Admin SDK integration
- ✅ Token verification middleware
- ✅ Protected endpoints (optional)
- ✅ Role-based authorization
- ✅ Firestore user profile storage

## 🚀 Quick Start Guide

### Step 1: Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click **"Add project"**
3. Enter project name: `edupath-optimizer`
4. (Optional) Enable Google Analytics
5. Click **"Create project"**

### Step 2: Enable Authentication
1. In Firebase Console, click **Authentication** in left menu
2. Click **"Get started"**
3. Go to **"Sign-in method"** tab
4. Enable **Email/Password**:
   - Click on it
   - Toggle "Enable"
   - Click "Save"
5. Enable **Google**:
   - Click on it
   - Toggle "Enable"
   - Enter project support email
   - Click "Save"

### Step 3: Create Firestore Database
1. Click **Firestore Database** in left menu
2. Click **"Create database"**
3. Select **"Start in production mode"** (we'll add rules)
4. Choose closest location
5. Click **"Enable"**

### Step 4: Setup Firestore Security Rules
1. In Firestore, go to **"Rules"** tab
2. Replace content with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow create: if request.auth != null && request.auth.uid == userId;
      allow update: if request.auth != null && request.auth.uid == userId;
    }
    
    // Student data (read for authenticated users, write for admins)
    match /students/{studentId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
  }
}
```

3. Click **"Publish"**

### Step 5: Get Firebase Web Config
1. Go to **Project Settings** (gear icon)
2. Scroll to **"Your apps"** section
3. Click the **Web icon** (</>) - "Add app"
4. Enter app nickname: `EduPath Web`
5. (Don't check Firebase Hosting for now)
6. Click **"Register app"**
7. Copy the `firebaseConfig` object (looks like this):

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

### Step 6: Update Frontend Config
1. Open: `frontend/config/firebase-config.json`
2. Replace with your config:

```json
{
  "apiKey": "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "authDomain": "your-project.firebaseapp.com",
  "projectId": "your-project-id",
  "storageBucket": "your-project.appspot.com",
  "messagingSenderId": "123456789012",
  "appId": "1:123456789012:web:abcdef123456"
}
```

### Step 7: (Optional) Backend Firebase Admin
For backend token verification:

1. Go to **Project Settings** → **Service Accounts**
2. Click **"Generate new private key"**
3. Save the JSON file as: `backend/firebase-admin-key.json`
4. Update `.env` file:
```
FIREBASE_CREDENTIALS_PATH=firebase-admin-key.json
```

### Step 8: Test Authentication
1. Start backend: `.\START.ps1`
2. Open: `http://localhost:5000/frontend/auth/signup.html` (or use file://)
3. Create a test account:
   - Full Name: Test Student
   - Email: test@example.com
   - Password: test123
   - Role: Student
4. Click "Create Account"
5. Should redirect to student dashboard

## 🧪 Testing the System

### Test Email/Password Login
```
Email: test@example.com
Password: test123
```

### Test Google Sign-In
1. Click "Sign in with Google"
2. Choose Google account
3. Grant permissions
4. Should auto-create profile and redirect

### Verify in Firebase Console
1. Go to **Authentication** → **Users** tab
2. You should see your registered users
3. Go to **Firestore Database**
4. Check `users` collection for user profiles

## 🔒 Security Features

### What's Protected:
✅ All user data encrypted in transit (HTTPS)
✅ Firebase ID tokens expire after 1 hour (auto-refresh)
✅ Firestore rules prevent unauthorized access
✅ Backend verifies tokens before serving data
✅ Passwords hashed by Firebase (bcrypt)
✅ SQL injection not possible (NoSQL database)

### What's NOT Protected (Demo Mode):
⚠️ If Firebase not configured, demo mode allows anonymous access
⚠️ Demo mode bypasses authentication
⚠️ Use Firebase for production deployment

## 📱 User Flows

### New User Registration:
1. User visits `signup.html`
2. Fills form → Submits
3. Firebase creates auth account
4. Profile created in Firestore (`users` collection)
5. Token stored in localStorage
6. Redirected to dashboard

### Existing User Login:
1. User visits `login.html`
2. Enters email/password → Submits
3. Firebase verifies credentials
4. Token retrieved and stored
5. User role fetched from Firestore
6. Redirected to appropriate dashboard

### Google OAuth Flow:
1. User clicks "Sign in with Google"
2. Google popup appears
3. User grants permissions
4. Firebase creates/updates account
5. Profile auto-created if new user
6. Redirected to dashboard

## 🎯 API Token Usage

### Frontend sends token in headers:
```javascript
fetch('http://localhost:5000/api/student/risk-assessment', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ random: true })
});
```

### Backend verifies token:
```python
@app.route('/api/protected', methods=['GET'])
@require_auth(role='admin')  # Only admins
def protected_route(user):
    # user object contains: uid, email, etc.
    return jsonify({'message': 'Authorized'})
```

## 🐛 Troubleshooting

### Error: "Firebase not configured"
**Solution**: Update `frontend/config/firebase-config.json` with your real config

### Error: "Unauthorized domain"
**Solution**: 
1. Go to Firebase Console → Authentication → Settings
2. Add your domain to "Authorized domains"
3. For local testing, `localhost` is automatically allowed

### Error: "Permission denied" in Firestore
**Solution**: Check Firestore rules are published correctly

### Users can't sign up
**Solution**: Make sure Email/Password is enabled in Authentication settings

### Google Sign-In not working
**Solution**: 
1. Check Google sign-in is enabled
2. Add OAuth 2.0 credentials if needed
3. Check authorized domains

## 📊 Firebase Console Monitoring

### Check active users:
Authentication → Users → See all registered users

### Check user profiles:
Firestore Database → `users` collection

### Check authentication logs:
Authentication → Usage (shows sign-in activity)

## 🚀 Going to Production

1. ✅ Enable Firebase App Check (for bot protection)
2. ✅ Set up custom domain in Firebase Hosting
3. ✅ Add all production domains to authorized domains
4. ✅ Rotate service account keys regularly
5. ✅ Enable Firebase Security Rules simulation testing
6. ✅ Set up Firebase monitoring and alerts
7. ✅ Never commit `firebase-config.json` to public repos
8. ✅ Use environment variables for sensitive data

## 💡 Current Status

**✅ READY TO USE**
- Login page: `frontend/auth/login.html`
- Signup page: `frontend/auth/signup.html`
- Backend auth: Fully implemented
- Demo mode: Works without Firebase

**⏳ PENDING (YOUR ACTION)**
- Create Firebase project
- Update `firebase-config.json`
- (Optional) Add Firebase Admin key for backend

**🎉 AFTER SETUP**
- Full authentication working
- Role-based access control
- Secure token management
- Production-ready security
