"""
ML Training Pipeline
Generates synthetic training data and trains the risk prediction model
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import json
import os
from ai_engine import FeatureEngineer, RiskPredictor


class TrainingPipeline:
    """
    Generates synthetic academic data and trains ML models
    """
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.risk_predictor = RiskPredictor()
    
    def generate_synthetic_dataset(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate realistic synthetic academic data
        
        Returns:
            X: Feature matrix
            y: Labels (0=pass, 1=fail)
        """
        np.random.seed(42)
        
        samples = []
        labels = []
        
        for i in range(n_samples):
            # Generate realistic student profile
            student_data = self._generate_student_profile(i)
            
            # Extract features
            features = self.feature_engineer.extract_features(student_data)
            samples.append(features)
            
            # Determine label based on realistic criteria
            label = self._determine_label(student_data)
            labels.append(label)
        
        X = np.array(samples)
        y = np.array(labels)
        
        return X, y
    
    def _generate_student_profile(self, student_id: int) -> Dict:
        """
        Generate a single realistic student profile with temporal patterns
        """
        # Determine student archetype
        archetype = np.random.choice([
            'excelling', 'stable', 'declining', 'struggling', 'recovering'
        ], p=[0.20, 0.35, 0.20, 0.15, 0.10])
        
        semester = np.random.randint(1, 9)
        
        # Generate attendance history based on archetype
        attendance_history = self._generate_attendance_pattern(archetype)
        
        # Generate marks history
        marks_history = self._generate_marks_pattern(archetype, semester)
        
        # Generate subjects
        num_subjects = np.random.randint(4, 8)
        all_subjects = [
            'Math', 'Physics', 'Chemistry', 'Programming', 'Data Structures',
            'Algorithms', 'Database', 'Networks', 'Operating Systems',
            'Software Engineering', 'Machine Learning', 'Web Development'
        ]
        current_subjects = np.random.choice(all_subjects, num_subjects, replace=False).tolist()
        
        # Previous failures
        if archetype == 'struggling':
            previous_failures = np.random.randint(2, 5)
        elif archetype == 'declining':
            previous_failures = np.random.randint(0, 2)
        elif archetype == 'recovering':
            previous_failures = np.random.randint(1, 3)
        else:
            previous_failures = np.random.randint(0, 2)
        
        return {
            'student_id': f'STU{student_id:04d}',
            'archetype': archetype,
            'attendance_history': attendance_history,
            'marks_history': marks_history,
            'current_subjects': current_subjects,
            'semester': semester,
            'previous_failures': previous_failures
        }
    
    def _generate_attendance_pattern(self, archetype: str) -> List[float]:
        """
        Generate realistic attendance trajectory over 12 weeks
        """
        weeks = 12
        
        if archetype == 'excelling':
            # High, stable attendance
            base = np.random.uniform(85, 95)
            trend = np.random.uniform(-0.2, 0.5)
            noise = 2
        elif archetype == 'stable':
            # Moderate, stable
            base = np.random.uniform(70, 85)
            trend = np.random.uniform(-0.5, 0.5)
            noise = 3
        elif archetype == 'declining':
            # Started ok, declining
            base = np.random.uniform(75, 85)
            trend = np.random.uniform(-1.5, -0.5)
            noise = 3
        elif archetype == 'struggling':
            # Low, unstable
            base = np.random.uniform(50, 70)
            trend = np.random.uniform(-1.0, 0.0)
            noise = 5
        else:  # recovering
            # Started low, improving
            base = np.random.uniform(60, 70)
            trend = np.random.uniform(0.5, 1.5)
            noise = 3
        
        attendance = []
        for week in range(weeks):
            value = base + trend * week + np.random.normal(0, noise)
            value = np.clip(value, 40, 100)
            attendance.append(round(value, 1))
        
        return attendance
    
    def _generate_marks_pattern(self, archetype: str, semester: int) -> List[Dict]:
        """
        Generate marks history for multiple subjects
        """
        num_subjects = np.random.randint(3, 6)
        marks_history = []
        
        for _ in range(num_subjects):
            num_tests = np.random.randint(3, 5)
            
            if archetype == 'excelling':
                base = np.random.uniform(16, 19)
                trend = np.random.uniform(-0.2, 0.5)
                noise = 1
            elif archetype == 'stable':
                base = np.random.uniform(12, 16)
                trend = np.random.uniform(-0.3, 0.3)
                noise = 1.5
            elif archetype == 'declining':
                base = np.random.uniform(14, 17)
                trend = np.random.uniform(-1.5, -0.5)
                noise = 1.5
            elif archetype == 'struggling':
                base = np.random.uniform(8, 13)
                trend = np.random.uniform(-0.8, 0.2)
                noise = 2
            else:  # recovering
                base = np.random.uniform(10, 14)
                trend = np.random.uniform(0.5, 1.5)
                noise = 1.5
            
            marks = []
            for test in range(num_tests):
                value = base + trend * test + np.random.normal(0, noise)
                value = np.clip(value, 0, 20)
                marks.append(round(value, 1))
            
            marks_history.append({
                'subject': f'Subject_{_}',
                'marks': marks
            })
        
        return marks_history
    
    def _determine_label(self, student_data: Dict) -> int:
        """
        Determine if student will fail based on realistic patterns
        NOT using hardcoded thresholds - using probabilistic logic
        """
        archetype = student_data['archetype']
        
        # Calculate risk factors
        attendance = student_data['attendance_history']
        recent_attendance = np.mean(attendance[-3:])
        attendance_trend = attendance[-1] - attendance[0]
        
        all_marks = []
        for subject in student_data['marks_history']:
            all_marks.extend(subject['marks'])
        avg_marks = np.mean(all_marks) if all_marks else 10
        
        prev_failures = student_data['previous_failures']
        
        # Probabilistic determination
        risk_score = 0.0
        
        # Attendance contribution
        if recent_attendance < 60:
            risk_score += 0.35
        elif recent_attendance < 75:
            risk_score += 0.20
        
        # Trend contribution (more important than snapshot)
        if attendance_trend < -15:
            risk_score += 0.25
        elif attendance_trend < -8:
            risk_score += 0.15
        
        # Performance contribution
        if avg_marks < 10:
            risk_score += 0.30
        elif avg_marks < 13:
            risk_score += 0.15
        
        # Historical failures
        risk_score += min(prev_failures * 0.10, 0.30)
        
        # Add some randomness
        risk_score += np.random.uniform(-0.1, 0.1)
        
        # Probabilistic label
        failure_threshold = np.random.uniform(0.45, 0.55)
        return 1 if risk_score > failure_threshold else 0
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """
        Train the risk prediction model
        """
        print(f"Training model on {len(X)} samples...")
        print(f"Feature dimensions: {X.shape[1]}")
        print(f"Failure rate: {np.mean(y)*100:.1f}%")
        
        metrics = self.risk_predictor.train(X, y)
        
        print(f"Training complete!")
        print(f"Training accuracy: {metrics['train_accuracy']:.3f}")
        print(f"Validation accuracy: {metrics['val_accuracy']:.3f}")
        
        return metrics
    
    def save_model(self, path: str = 'ml_models/risk_predictor.pkl'):
        """Save trained model"""
        self.risk_predictor.save_model()
        print(f"Model saved to {path}")
    
    def export_sample_data(self, n_samples: int = 50, 
                            output_path: str = 'data/sample_students.json'):
        """
        Export sample student data for demonstration
        """
        samples = []
        
        for i in range(n_samples):
            student_data = self._generate_student_profile(i)
            
            # Add prediction
            features = self.feature_engineer.extract_features(student_data)
            prediction = self.risk_predictor.predict(features)
            
            student_data['prediction'] = prediction
            samples.append(student_data)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(samples, f, indent=2)
        
        print(f"Exported {n_samples} sample students to {output_path}")


if __name__ == '__main__':
    # Training script
    print("=" * 60)
    print("EduPath Optimizer - ML Training Pipeline")
    print("=" * 60)
    
    pipeline = TrainingPipeline()
    
    # Generate synthetic data
    print("\n1. Generating synthetic training data...")
    X, y = pipeline.generate_synthetic_dataset(n_samples=2000)
    
    # Train model
    print("\n2. Training risk prediction model...")
    metrics = pipeline.train_model(X, y)
    
    # Save model
    print("\n3. Saving model...")
    pipeline.save_model()
    
    # Export sample data
    print("\n4. Exporting sample data...")
    pipeline.export_sample_data(n_samples=100)
    
    print("\n" + "=" * 60)
    print("Training pipeline complete!")
    print("=" * 60)
