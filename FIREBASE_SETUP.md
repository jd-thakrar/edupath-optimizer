# Firebase Setup Guide

## Prerequisites
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing project
3. Enable Authentication → Email/Password and Google Sign-In

## Configuration Steps

### 1. Get Firebase Config
1. In Firebase Console, go to **Project Settings** (gear icon)
2. Scroll down to **Your apps** section
3. Click **Web app** icon (</>) to add a web app
4. Copy the `firebaseConfig` object

### 2. Update Frontend Config
Open `frontend/config/firebase-config.json` and replace with your config:

```json
{
  "apiKey": "AIzaSy...",
  "authDomain": "your-project.firebaseapp.com",
  "projectId": "your-project-id",
  "storageBucket": "your-project.appspot.com",
  "messagingSenderId": "123456789",
  "appId": "1:123456789:web:abc123"
}
```

### 3. Setup Firestore Database
1. In Firebase Console, go to **Firestore Database**
2. Click **Create database**
3. Start in **production mode** (or test mode for development)
4. Choose a location close to your users

### 4. Configure Firestore Rules
Replace the content of Firestore rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      // Users can read their own data
      allow read: if request.auth != null && request.auth.uid == userId;
      // Only authenticated users can create their profile
      allow create: if request.auth != null && request.auth.uid == userId;
      // Users can update their own data
      allow update: if request.auth != null && request.auth.uid == userId;
    }
    
    // Student data collection
    match /students/{studentId} {
      // Allow read if authenticated
      allow read: if request.auth != null;
      // Only admins can write
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
  }
}
```

### 5. Enable Authentication Methods
1. Go to **Authentication** → **Sign-in method**
2. Enable **Email/Password**
3. Enable **Google** (add OAuth 2.0 credentials)

### 6. Backend Firebase Admin Setup (Optional)
For token verification on backend:

1. Generate a service account key:
   - Go to **Project Settings** → **Service Accounts**
   - Click **Generate new private key**
   - Save the JSON file as `backend/firebase-admin-key.json`

2. The backend will automatically use this for Firebase Admin SDK

## Features Enabled

✅ **Email/Password Authentication**
- User registration with email and password
- Secure login with Firebase
- Password reset (can be implemented)

✅ **Google Sign-In**
- One-click authentication with Google account
- Automatic profile creation

✅ **User Roles**
- Student role (default)
- Admin role (for administrators)
- Role-based dashboard redirection

✅ **Secure Token Management**
- Firebase ID tokens stored in localStorage
- Automatic token refresh
- Backend token verification (if configured)

✅ **User Profile in Firestore**
- Stores: uid, email, displayName, role, createdAt
- Enrollment ID auto-generated
- Semester tracking

## Demo Mode
If Firebase is not configured, the system falls back to demo mode:
- Click "Demo Student" or "Demo Admin" buttons
- No authentication required
- All features work with random student data

## Testing
1. Open `frontend/auth/signup.html`
2. Create a test account
3. Login with created credentials
4. Verify dashboard access

## Troubleshooting

**Error: Firebase not configured**
→ Check if `firebase-config.json` has valid credentials

**Error: Unauthorized domain**
→ Add your domain to Firebase Console → Authentication → Settings → Authorized domains

**Error: Insufficient permissions**
→ Check Firestore rules and user role

## Security Notes
- Never commit `firebase-config.json` with real credentials to public repos
- Use environment variables in production
- Implement proper Firestore security rules
- Enable App Check for additional security
- Rotate service account keys regularly
