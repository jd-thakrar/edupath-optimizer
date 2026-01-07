"""
Risk Prediction Model - Probabilistic ML-based failure prediction
Uses Gradient Boosting for pattern learning
"""

import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from typing import Dict, Tuple, Any
import os


class RiskPredictor:
    """
    Probabilistic risk prediction model
    Returns failure probability with confidence score
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.calibrated_model = None
        self.model_path = model_path or 'ml_models/risk_predictor.pkl'
        self.is_trained = False
        
        # Load existing model if available
        if os.path.exists(self.model_path):
            self.load_model()
    
    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Train the risk prediction model
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Binary labels (0=pass, 1=fail)
        
        Returns:
            Training metrics
        """
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Gradient Boosting Classifier
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=10,
            min_samples_leaf=5,
            subsample=0.8,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Calibrate probabilities for better confidence estimation
        # Use validation set directly instead of prefit mode
        self.calibrated_model = CalibratedClassifierCV(
            estimator=GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=5,
                subsample=0.8,
                random_state=42
            ),
            method='sigmoid',
            cv=5
        )
        # Combine train and val for calibration
        X_combined = np.vstack([X_train, X_val])
        y_combined = np.hstack([y_train, y_val])
        self.calibrated_model.fit(X_combined, y_combined)
        
        self.is_trained = True
        
        # Compute metrics
        train_score = self.model.score(X_train, y_train)
        val_score = self.model.score(X_val, y_val)
        
        return {
            'train_accuracy': float(train_score),
            'val_accuracy': float(val_score),
            'n_samples': len(X),
            'n_features': X.shape[1]
        }
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Predict failure risk with confidence
        
        Args:
            features: Feature vector (1, n_features) or (n_features,)
        
        Returns:
            {
                'failure_probability': float [0, 1],
                'confidence': float [0, 1],
                'risk_level': str,
                'prediction': int (0 or 1)
            }
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a trained model.")
        
        # Reshape if needed
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        # Get calibrated probability
        proba = self.calibrated_model.predict_proba(features)[0]
        failure_prob = float(proba[1])  # Probability of failure
        
        # Compute confidence based on probability distance from 0.5
        # Higher confidence when probability is closer to 0 or 1
        confidence = float(abs(failure_prob - 0.5) * 2)
        
        # Determine risk level (no hardcoded thresholds for decisions, only for labels)
        if failure_prob >= 0.7:
            risk_level = "high"
        elif failure_prob >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        prediction = int(failure_prob >= 0.5)
        
        return {
            'failure_probability': round(failure_prob, 4),
            'confidence': round(confidence, 4),
            'risk_level': risk_level,
            'prediction': prediction
        }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores for interpretability
        """
        if not self.is_trained:
            return {}
        
        importances = self.model.feature_importances_
        return {f'feature_{i}': float(imp) for i, imp in enumerate(importances)}
    
    def save_model(self):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'calibrated_model': self.calibrated_model
        }, self.model_path)
    
    def load_model(self):
        """Load trained model from disk"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"No model found at {self.model_path}")
        
        loaded = joblib.load(self.model_path)
        self.model = loaded['model']
        self.calibrated_model = loaded['calibrated_model']
        self.is_trained = True
    
    def predict_batch(self, features_batch: np.ndarray) -> list:
        """
        Predict risk for multiple students
        
        Args:
            features_batch: Feature matrix (n_students, n_features)
        
        Returns:
            List of prediction dictionaries
        """
        predictions = []
        for features in features_batch:
            predictions.append(self.predict(features))
        return predictions
