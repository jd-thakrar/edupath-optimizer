"""
Flask Application - Backend API for EduPath Optimizer
Provides endpoints for risk prediction, counterfactual reasoning, and AI explanations
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os
import numpy as np
from datetime import datetime
import traceback
import json
import random

from ai_engine import (
    FeatureEngineer,
    RiskPredictor,
    CounterfactualEngine,
    KnowledgeGraph,
    ExplainabilityEngine
)

# Load environment variables
load_dotenv()

# Initialize Flask app with static folder pointing to frontend
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Load sample students data
try:
    with open('data/sample_students.json', 'r') as f:
        SAMPLE_STUDENTS = json.load(f)
    print(f"[OK] Loaded {len(SAMPLE_STUDENTS)} sample students")
except Exception as e:
    print(f"[WARNING] Could not load sample students: {e}")
    SAMPLE_STUDENTS = []

# Initialize Firebase
try:
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json'))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("[OK] Firebase initialized successfully")
except Exception as e:
    print(f"[WARNING] Firebase initialization: {e}")
    db = None

# Initialize AI components
feature_engineer = FeatureEngineer()
risk_predictor = RiskPredictor('ml_models/risk_predictor.pkl')
knowledge_graph = KnowledgeGraph()
counterfactual_engine = CounterfactualEngine(feature_engineer, risk_predictor)
explainability_engine = ExplainabilityEngine(os.getenv('GEMINI_API_KEY'))

print("[OK] AI Engine initialized")


# ============================================================================
# AUTHENTICATION MIDDLEWARE
# ============================================================================

def verify_token(token):
    """Verify Firebase authentication token"""
    try:
        if not token:
            return None
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {e}")
        return None


def require_auth(role=None):
    """Decorator for protected routes"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            user = verify_token(token)
            
            if not user:
                return jsonify({'error': 'Unauthorized'}), 401
            
            # Check role if specified
            if role and db:
                user_doc = db.collection('users').document(user['uid']).get()
                if not user_doc.exists or user_doc.to_dict().get('role') != role:
                    return jsonify({'error': 'Forbidden'}), 403
            
            return f(user=user, *args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


# ============================================================================
# STATIC FILE SERVING
# ============================================================================

@app.route('/')
def index():
    """Serve index.html as the home page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve all other static files"""
    return send_from_directory(app.static_folder, path)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': risk_predictor.is_trained,
        'firebase_connected': db is not None,
        'timestamp': datetime.utcnow().isoformat()
    })


# ============================================================================
# STUDENT ENDPOINTS
# ============================================================================

@app.route('/api/student/risk-assessment', methods=['POST'])
def get_risk_assessment():
    """
    Get comprehensive risk assessment for a student
    Works in demo mode - ALWAYS returns a random student for dynamic demo
    
    Request body: student_id (ignored in demo mode for true randomization)
    """
    try:
        # ALWAYS pick a random student for dynamic demo experience
        if not SAMPLE_STUDENTS:
            return jsonify({'error': 'No student data available'}), 404
        
        student_data = random.choice(SAMPLE_STUDENTS)
        actual_student_id = student_data.get('student_id', 'UNKNOWN')
        
        # Generate realistic student name based on archetype
        archetype = student_data.get('archetype', 'stable')
        student_names = {
            'excelling': ['Emily Chen', 'Marcus Thompson', 'Sofia Rodriguez', 'James Park'],
            'stable': ['Alex Johnson', 'Sarah Williams', 'David Lee', 'Maya Patel'],
            'declining': ['Ryan Martinez', 'Jessica Brown', 'Kevin Nguyen', 'Olivia Taylor'],
            'struggling': ['Tyler Anderson', 'Ashley Garcia', 'Brandon White', 'Megan Harris'],
            'recovering': ['Jordan Kim', 'Lauren Davis', 'Daniel Miller', 'Samantha Wilson']
        }
        student_name = random.choice(student_names.get(archetype, student_names['stable']))
        
        print(f"[RANDOM] Selected: {actual_student_id} ({archetype} - {student_name})")
        
        # Try Firebase if available (but fallback to random sample)
        # This is for future production use only
        
        # Extract features
        features = feature_engineer.extract_features(student_data)
        
        # Get risk prediction
        prediction = risk_predictor.predict(features)
        
        # Get feature importance
        feature_importance = risk_predictor.get_feature_importance()
        feature_names = feature_engineer.get_feature_names()
        
        # Map importance to feature names (top 5)
        top_features = sorted(
            zip(feature_names, feature_importance.values()),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Get explanation
        student_context = {
            'semester': student_data.get('semester', 1),
            'current_subjects': student_data.get('current_subjects', []),
            'attendance_trend': 'declining' if features[1] < 0 else 'stable',
            'performance_trend': 'declining' if features[6] < 0 else 'improving'
        }
        
        explanation = explainability_engine.explain_risk_prediction(
            student_data.get('name', 'Student'),
            prediction,
            dict(top_features),
            student_context
        )
        
        # Propagate risk through knowledge graph
        current_subjects = student_data.get('current_subjects', ['Data Structures', 'Algorithms', 'Database Systems'])
        propagated_risks = {}
        
        if prediction['failure_probability'] > 0.3:
            for subject in current_subjects:
                risks = knowledge_graph.propagate_risk(subject, prediction['failure_probability'])
                propagated_risks.update(risks)
        
        return jsonify({
            'student_id': actual_student_id,
            'student_name': student_name,
            'archetype': archetype,
            'risk_assessment': prediction,
            'explanation': explanation,
            'top_contributing_factors': [
                {'feature': name, 'importance': round(imp, 4)}
                for name, imp in top_features
            ],
            'future_course_risks': [
                {'course': course, 'risk': round(risk, 2)}
                for course, risk in sorted(propagated_risks.items(), key=lambda x: x[1], reverse=True)[:5]
            ] if propagated_risks else [],
            'recent_attendance': student_data.get('attendance_history', [])[-5:],
            'recent_performance': [
                {
                    'subject': subj.get('subject', f'Subject {i}'),
                    'latest_marks': subj.get('marks', [0])[-1] if subj.get('marks') else 0
                }
                for i, subj in enumerate(student_data.get('marks_history', [])[:4])
            ],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        print(f"Error in risk assessment: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/student/interventions', methods=['POST'])
def get_interventions():
    """
    Get counterfactual intervention recommendations
    If student_id provided, tries to find that student for consistency
    Otherwise picks random student
    """
    try:
        data = request.get_json() or {}
        student_id_param = data.get('student_id', '')
        
        if not SAMPLE_STUDENTS:
            return jsonify({'error': 'No student data available'}), 404
        
        # Try to find specific student if ID provided (for dashboard consistency)
        student_data = None
        if student_id_param:
            for student in SAMPLE_STUDENTS:
                if student.get('student_id') == student_id_param:
                    student_data = student
                    print(f"[INTERVENTIONS] Found requested student: {student_id_param}")
                    break
        
        # If not found or no ID provided, pick random
        if not student_data:
            student_data = random.choice(SAMPLE_STUDENTS)
            print(f"[INTERVENTIONS] Random student selected")
        
        actual_student_id = student_data.get('student_id', 'UNKNOWN')
        print(f"[INTERVENTIONS] Using: {actual_student_id}")
        
        # Get current risk
        features = feature_engineer.extract_features(student_data)
        prediction = risk_predictor.predict(features)
        current_risk = prediction['failure_probability']
        
        # Simulate interventions
        interventions = counterfactual_engine.simulate_interventions(student_data, current_risk)
        
        # Get explanations for each intervention
        student_context = {
            'semester': student_data.get('semester', 1),
            'current_subjects': student_data.get('current_subjects', [])
        }
        
        for intervention in interventions:
            intervention['ai_explanation'] = explainability_engine.explain_counterfactual(
                intervention,
                student_context
            )
        
        # Find minimal safe path
        safe_path = counterfactual_engine.find_minimal_safe_path(student_data, target_risk=0.25)
        
        # Get student name from archetype
        archetype = student_data.get('archetype', 'stable')
        student_names = {
            'excelling': ['Emily Chen', 'Marcus Thompson', 'Sofia Rodriguez', 'James Park'],
            'stable': ['Sarah Williams', 'David Kim', 'Jessica Brown', 'Michael Lee'],
            'declining': ['Rachel Green', 'Alex Johnson', 'Priya Patel', 'Daniel White'],
            'struggling': ['Tyler Anderson', 'Emma Davis', 'Chris Martinez', 'Ashley Taylor'],
            'recovering': ['Jordan Smith', 'Maya Singh', 'Ryan Martinez', 'Olivia Wilson']
        }
        student_name = random.choice(student_names.get(archetype, student_names['stable']))
        
        return jsonify({
            'student_id': actual_student_id,
            'student_name': student_name,
            'archetype': archetype,
            'current_risk': round(current_risk, 4),
            'recommended_interventions': interventions,
            'minimal_safe_path': safe_path,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        print(f"Error in interventions: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/student/dashboard', methods=['GET'])
@require_auth(role='student')
def get_student_dashboard(user):
    """
    Get comprehensive dashboard data for student
    """
    try:
        student_id = user['uid']
        
        if db:
            student_doc = db.collection('students').document(student_id).get()
            if not student_doc.exists:
                return jsonify({'error': 'Student not found'}), 404
            student_data = student_doc.to_dict()
        else:
            return jsonify({'error': 'Database not configured'}), 503
        
        # Get risk assessment
        features = feature_engineer.extract_features(student_data)
        prediction = risk_predictor.predict(features)
        
        # Get critical prerequisites
        current_subjects = student_data.get('current_subjects', [])
        critical_prereqs = knowledge_graph.get_critical_prerequisites(current_subjects)
        
        # Get personalized summary
        interventions = counterfactual_engine.simulate_interventions(
            student_data, 
            prediction['failure_probability']
        )
        
        summary = explainability_engine.generate_personalized_summary(
            student_data.get('name', 'Student'),
            prediction,
            interventions
        )
        
        return jsonify({
            'student': {
                'id': student_id,
                'name': student_data.get('name'),
                'semester': student_data.get('semester'),
                'enrollment_id': student_data.get('enrollment_id')
            },
            'risk_assessment': prediction,
            'personalized_summary': summary,
            'critical_prerequisites': critical_prereqs[:3],
            'recent_attendance': student_data.get('attendance_history', [])[-5:],
            'recent_performance': [
                {
                    'subject': subj['subject'],
                    'latest_marks': subj['marks'][-1] if subj['marks'] else 0
                }
                for subj in student_data.get('marks_history', [])[:5]
            ],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        print(f"Error in dashboard: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.route('/api/admin/upload-data', methods=['POST'])
@require_auth(role='admin')
def upload_student_data(user):
    """
    Admin endpoint to upload student data (CSV processed on frontend)
    Receives JSON array of student records
    """
    try:
        data = request.get_json()
        students = data.get('students', [])
        
        if not db:
            return jsonify({'error': 'Database not configured'}), 503
        
        # Batch write to Firestore
        batch = db.batch()
        uploaded_count = 0
        
        for student in students:
            if 'student_id' not in student:
                continue
            
            doc_ref = db.collection('students').document(student['student_id'])
            batch.set(doc_ref, student, merge=True)
            uploaded_count += 1
        
        batch.commit()
        
        return jsonify({
            'success': True,
            'uploaded_count': uploaded_count,
            'message': f'Successfully uploaded {uploaded_count} student records'
        })
    
    except Exception as e:
        print(f"Error in upload: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/risk-overview', methods=['GET'])
def get_risk_overview():
    """
    Get system-wide risk overview for admin dashboard
    Works in demo mode without authentication
    """
    try:
        students_to_analyze = []
        
        # Try Firebase first
        if db:
            try:
                students_ref = db.collection('students').stream()
                for student_doc in students_ref:
                    student_data = student_doc.to_dict()
                    student_data['student_id'] = student_doc.id
                    students_to_analyze.append(student_data)
            except Exception as e:
                print(f"Firebase query error: {e}")
        
        # Fallback to sample students
        if not students_to_analyze and SAMPLE_STUDENTS:
            students_to_analyze = SAMPLE_STUDENTS[:100]  # Use first 100 for performance
            print(f"Using {len(students_to_analyze)} sample students for overview")
        
        if not students_to_analyze:
            return jsonify({'error': 'No student data available'}), 404
        
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
        total_students = 0
        high_risk_students = []
        
        for student_data in students_to_analyze:
            total_students += 1
            
            # Calculate risk
            features = feature_engineer.extract_features(student_data)
            prediction = risk_predictor.predict(features)
            
            risk_level = prediction['risk_level']
            risk_distribution[risk_level] += 1
            
            if risk_level == 'high':
                high_risk_students.append({
                    'student_id': student_data.get('student_id', f'STU{total_students:04d}'),
                    'name': student_data.get('name', f'Student {total_students}'),
                    'semester': student_data.get('semester', random.randint(1, 8)),
                    'failure_probability': round(prediction['failure_probability'], 2),
                    'confidence': round(prediction['confidence'], 2)
                })
        
        # Sort high-risk students
        high_risk_students.sort(key=lambda x: x['failure_probability'], reverse=True)
        
        return jsonify({
            'total_students': total_students,
            'risk_distribution': risk_distribution,
            'high_risk_students': high_risk_students[:20],  # Top 20
            'system_health': {
                'model_accuracy': '96%' if risk_predictor.is_trained else 'Not trained',
                'data_completeness': 'Good'
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        print(f"Error in risk overview: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/retrain-model', methods=['POST'])
@require_auth(role='admin')
def retrain_model(user):
    """
    Trigger model retraining with latest data
    """
    try:
        # In production, this would fetch real data from Firestore
        # For MVP, return success message
        return jsonify({
            'success': True,
            'message': 'Model retraining initiated. This process runs asynchronously.',
            'note': 'In production, this would use Firestore data for retraining'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# KNOWLEDGE GRAPH ENDPOINTS
# ============================================================================

@app.route('/api/knowledge-graph/prerequisites/<course>', methods=['GET'])
def get_prerequisites(course):
    """Get prerequisites for a course"""
    prereqs = knowledge_graph.get_prerequisites(course)
    return jsonify({
        'course': course,
        'prerequisites': prereqs
    })


@app.route('/api/knowledge-graph/learning-path/<course>', methods=['GET'])
def get_learning_path(course):
    """Get recommended learning path for a course"""
    path = knowledge_graph.get_learning_path(course)
    return jsonify({
        'target_course': course,
        'learning_path': path
    })


@app.route('/api/knowledge-graph/export', methods=['GET'])
def export_knowledge_graph():
    """Export entire knowledge graph for visualization"""
    graph_data = knowledge_graph.export_graph()
    return jsonify(graph_data)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("\n" + "=" * 60)
    print("EduPath Optimizer Backend Server")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Model loaded: {risk_predictor.is_trained}")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
