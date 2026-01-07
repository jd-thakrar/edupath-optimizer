# 🚀 Quick Start Guide - EduPath Optimizer

Get the system running in 10 minutes!

---

## ⚡ Quick Demo (No Setup Required)

1. **Open Frontend:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Navigate to: `http://localhost:8000`

2. **Click "Login" → Select "Student" Demo**
   - Explore dashboard with demo data
   - View AI recommendations
   - Test simulation playground

3. **Try Admin View:**
   - Logout and select "Admin" demo
   - View system-wide risk overview

**Note:** Demo mode uses pre-loaded data, no backend required!

---

## 🔧 Full System Setup (15 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the ML Model
```bash
cd backend
python train_model.py
```

**Expected Output:**
```
Training model on 2000 samples...
Feature dimensions: 22
Failure rate: 42.3%
Training complete!
Training accuracy: 0.892
Validation accuracy: 0.873
Model saved to ml_models/risk_predictor.pkl
```

### Step 3: Configure Environment
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```bash
GEMINI_API_KEY=your_key_here  # Get from: https://makersuite.google.com/app/apikey
FIREBASE_PROJECT_ID=your_project_id
```

### Step 4: Start Backend
```bash
cd backend
python app.py
```

Server runs on `http://localhost:5000`

### Step 5: Update Frontend API URL
Edit `frontend/student/dashboard.html` (line ~380):
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Step 6: Open Frontend
```bash
cd frontend
python -m http.server 8000
```

Navigate to `http://localhost:8000`

---

## 🧪 Test the AI Engine

### Test Risk Prediction
```bash
cd backend
python
```

```python
from ai_engine import FeatureEngineer, RiskPredictor
import numpy as np

# Load model
predictor = RiskPredictor('ml_models/risk_predictor.pkl')
feature_engineer = FeatureEngineer()

# Sample student data
student_data = {
    'attendance_history': [78, 76, 72, 70, 68],
    'marks_history': [
        {'subject': 'Math', 'marks': [15, 14, 13]},
        {'subject': 'Physics', 'marks': [16, 15, 14]}
    ],
    'current_subjects': ['Math', 'Physics', 'Chemistry'],
    'semester': 3,
    'previous_failures': 0
}

# Extract features and predict
features = feature_engineer.extract_features(student_data)
prediction = predictor.predict(features)

print(prediction)
# Output:
# {
#   'failure_probability': 0.38,
#   'confidence': 0.82,
#   'risk_level': 'medium',
#   'prediction': 0
# }
```

### Test Counterfactual Engine
```python
from ai_engine import CounterfactualEngine

cf_engine = CounterfactualEngine(feature_engineer, predictor)

# Simulate interventions
interventions = cf_engine.simulate_interventions(
    student_data, 
    current_risk=0.38
)

for i in interventions:
    print(f"{i['action']}: {i['risk_reduction_percent']}% reduction")
```

---

## 📦 Project Structure

```
EDU/
├── backend/
│   ├── ai_engine/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py      # 22 features extraction
│   │   ├── risk_predictor.py           # Gradient Boosting model
│   │   ├── counterfactual_engine.py    # What-if simulations
│   │   ├── knowledge_graph.py          # Prerequisite dependencies
│   │   └── explainability.py           # Gemini API integration
│   ├── app.py                          # Flask API server
│   ├── train_model.py                  # ML training pipeline
│   └── .env.example                    # Environment template
│
├── frontend/
│   ├── index.html                      # Landing page
│   ├── auth/
│   │   └── login.html                  # Authentication
│   ├── student/
│   │   ├── dashboard.html              # Student dashboard
│   │   └── insights.html               # AI recommendations
│   └── admin/
│       └── dashboard.html              # Admin panel
│
├── ml_models/
│   └── risk_predictor.pkl              # Trained model (generated)
│
├── data/
│   └── sample_students.json            # Sample data (generated)
│
├── requirements.txt                     # Python dependencies
├── Dockerfile                          # Container configuration
├── firebase.json                       # Firebase config
├── firestore.rules                     # Security rules
├── FIRESTORE_SCHEMA.md                 # Database documentation
├── README.md                           # Full documentation
└── QUICKSTART.md                       # This file
```

---

## 🎯 Key Files Explained

### AI Engine Core
- **feature_engineering.py** - Extracts temporal patterns from raw data
- **risk_predictor.py** - ML model for probabilistic predictions
- **counterfactual_engine.py** - Simulates "what-if" scenarios
- **knowledge_graph.py** - Models course dependencies
- **explainability.py** - Gemini API for natural language

### Backend API
- **app.py** - Flask server with all endpoints
- **train_model.py** - Generates synthetic data and trains model

### Frontend
- **dashboard.html** - Risk visualization, trends, AI explanation
- **insights.html** - Counterfactual recommendations, simulation
- **admin/dashboard.html** - System overview, data upload

---

## 🔑 Firebase Setup (Optional)

### 1. Create Firebase Project
Visit: https://console.firebase.google.com/

### 2. Enable Services
- Authentication (Email/Password)
- Firestore Database
- Hosting

### 3. Get Credentials
- Download service account key → Save as `firebase-credentials.json`
- Copy Firebase config → Update in `frontend/auth/login.html`

### 4. Deploy Rules
```bash
firebase deploy --only firestore:rules
```

---

## 🐛 Troubleshooting

### Model Not Found Error
```
FileNotFoundError: No model found at ml_models/risk_predictor.pkl
```
**Solution:** Run `python backend/train_model.py` first

### Firebase Connection Error
```
Firebase initialization warning: ...
```
**Solution:** Set up Firebase credentials or use demo mode

### Gemini API Error
```
Gemini API error: Invalid API key
```
**Solution:** Get API key from https://makersuite.google.com/app/apikey

### Import Error
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution:** `pip install -r requirements.txt`

---

## 📊 Understanding the Output

### Risk Assessment
```json
{
  "failure_probability": 0.38,  // 38% chance of failing
  "confidence": 0.82,            // Model is 82% certain
  "risk_level": "medium"         // Categorical label
}
```

### Counterfactual Recommendation
```json
{
  "action": "Improve Attendance",
  "description": "Attend 15% more classes",
  "current_risk": 0.38,
  "predicted_risk": 0.22,        // After intervention
  "risk_reduction": 0.16,        // 16% absolute reduction
  "effort_level": 2,             // On scale of 1-5
  "effectiveness_score": 0.08    // risk_reduction / effort
}
```

---

## 🎓 Next Steps

1. **Explore the Code:**
   - Read comments in `backend/ai_engine/`
   - Understand feature engineering logic
   - Study counterfactual simulation

2. **Customize for Your Institution:**
   - Modify knowledge graph with actual courses
   - Adjust feature weights based on your data
   - Train on real historical data

3. **Deploy to Production:**
   - Follow deployment guide in README.md
   - Set up Firebase properly
   - Configure environment variables

4. **Extend Functionality:**
   - Add more intervention types
   - Implement real-time alerts
   - Create mobile app

---

## 💡 Pro Tips

1. **Model Retraining:**
   - Retrain quarterly with new data
   - Monitor prediction accuracy
   - Adjust hyperparameters if needed

2. **Feature Importance:**
   - Check `predictor.get_feature_importance()`
   - Focus interventions on top features

3. **Simulation Playground:**
   - Use to educate students about risk factors
   - Demonstrate impact of small changes

4. **Admin Dashboard:**
   - Export high-risk student reports
   - Track intervention effectiveness

---

## 🏆 Success Indicators

You've successfully set up the system when:
- ✅ Model trains with 85%+ accuracy
- ✅ API returns predictions in <500ms
- ✅ Frontend displays risk visualizations
- ✅ Counterfactual engine generates recommendations
- ✅ Gemini explanations are context-aware

---

**Questions? Check README.md for detailed documentation!**
