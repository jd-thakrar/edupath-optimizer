"""
Feature Engineering Layer for EduPath Optimizer
Extracts intelligent features from raw academic data
NO hardcoded thresholds - pure pattern extraction
"""

import numpy as np
from typing import Dict, List, Any
from scipy.stats import linregress


class FeatureEngineer:
    """
    Transforms raw academic data into ML-ready features
    Focuses on temporal patterns, not snapshots
    """
    
    def __init__(self):
        self.feature_names = []
    
    def extract_features(self, student_data: Dict[str, Any]) -> np.ndarray:
        """
        Extract all features for a single student
        
        Args:
            student_data: {
                'attendance_history': [75, 72, 68, 65, 62],  # weekly percentages
                'marks_history': [
                    {'subject': 'Math', 'marks': [15, 17, 14]},  # internal marks
                    {'subject': 'Physics', 'marks': [18, 16, 15]}
                ],
                'current_subjects': ['Math', 'Physics', 'Chemistry'],
                'semester': 3,
                'previous_failures': 1
            }
        
        Returns:
            Feature vector as numpy array
        """
        features = []
        
        # 1. ATTENDANCE FEATURES (temporal patterns)
        attendance = student_data.get('attendance_history', [])
        features.extend(self._extract_attendance_features(attendance))
        
        # 2. MARKS FEATURES (performance trajectory)
        marks = student_data.get('marks_history', [])
        features.extend(self._extract_marks_features(marks))
        
        # 3. ACADEMIC LOAD FEATURES
        current_subjects = student_data.get('current_subjects', [])
        semester = student_data.get('semester', 1)
        features.extend(self._extract_load_features(current_subjects, semester))
        
        # 4. HISTORICAL FEATURES
        prev_failures = student_data.get('previous_failures', 0)
        features.append(prev_failures)
        features.append(prev_failures / max(semester, 1))  # failure rate
        
        # 5. ENGAGEMENT FEATURES
        features.extend(self._extract_engagement_features(attendance, marks))
        
        return np.array(features, dtype=np.float32)
    
    def _extract_attendance_features(self, attendance: List[float]) -> List[float]:
        """
        Extract temporal attendance patterns
        NOT just current value - TREND matters
        """
        if len(attendance) < 2:
            return [0.0] * 6
        
        attendance = np.array(attendance)
        
        # Current attendance (normalized)
        current = attendance[-1] / 100.0
        
        # Attendance trend (slope) - CRITICAL
        weeks = np.arange(len(attendance))
        slope, _, _, _, _ = linregress(weeks, attendance)
        trend = slope / 10.0  # normalize
        
        # Attendance volatility (standard deviation)
        volatility = np.std(attendance) / 100.0
        
        # Recent vs early comparison
        recent_mean = np.mean(attendance[-3:]) if len(attendance) >= 3 else attendance[-1]
        early_mean = np.mean(attendance[:3]) if len(attendance) >= 3 else attendance[0]
        decline = (early_mean - recent_mean) / 100.0
        
        # Consecutive declining weeks
        declines = 0
        for i in range(1, len(attendance)):
            if attendance[i] < attendance[i-1]:
                declines += 1
        decline_ratio = declines / len(attendance)
        
        # Minimum attendance reached
        min_attendance = np.min(attendance) / 100.0
        
        return [current, trend, volatility, decline, decline_ratio, min_attendance]
    
    def _extract_marks_features(self, marks_history: List[Dict]) -> List[float]:
        """
        Extract performance trajectory features per subject
        """
        if not marks_history:
            return [0.0] * 8
        
        all_trends = []
        all_volatilities = []
        all_means = []
        all_recent = []
        
        for subject_data in marks_history:
            marks = subject_data.get('marks', [])
            if len(marks) < 2:
                continue
            
            marks_arr = np.array(marks)
            
            # Trend
            tests = np.arange(len(marks))
            slope, _, _, _, _ = linregress(tests, marks_arr)
            all_trends.append(slope)
            
            # Volatility
            all_volatilities.append(np.std(marks_arr))
            
            # Mean performance
            all_means.append(np.mean(marks_arr))
            
            # Recent performance
            all_recent.append(np.mean(marks_arr[-2:]) if len(marks_arr) >= 2 else marks_arr[-1])
        
        # Aggregate across subjects
        avg_trend = np.mean(all_trends) / 10.0 if all_trends else 0.0
        avg_volatility = np.mean(all_volatilities) / 20.0 if all_volatilities else 0.0
        avg_performance = np.mean(all_means) / 20.0 if all_means else 0.0
        recent_performance = np.mean(all_recent) / 20.0 if all_recent else 0.0
        
        # Subject count with declining trend
        declining_subjects = sum(1 for t in all_trends if t < -0.5)
        declining_ratio = declining_subjects / max(len(marks_history), 1)
        
        # Performance consistency
        performance_range = (max(all_means) - min(all_means)) / 20.0 if all_means else 0.0
        
        # Weak subjects count (below median)
        median_perf = np.median(all_means) if all_means else 0
        weak_subjects = sum(1 for m in all_means if m < median_perf)
        weak_ratio = weak_subjects / max(len(marks_history), 1)
        
        return [
            avg_trend, avg_volatility, avg_performance, recent_performance,
            declining_ratio, performance_range, weak_ratio, len(marks_history)
        ]
    
    def _extract_load_features(self, subjects: List[str], semester: int) -> List[float]:
        """
        Academic load and difficulty features
        """
        subject_count = len(subjects)
        
        # Semester progression (higher = more complex)
        semester_factor = semester / 8.0  # normalize by max semesters
        
        # Load intensity
        load_intensity = subject_count / 6.0  # normalize by typical load
        
        # Subject difficulty estimation (simplified for MVP)
        # In production, this would come from historical data
        difficulty_map = {
            'Math': 0.9, 'Calculus': 0.95, 'Linear Algebra': 0.85,
            'Physics': 0.85, 'Chemistry': 0.80, 'Programming': 0.88,
            'Data Structures': 0.90, 'Algorithms': 0.92,
            'Database': 0.75, 'Networks': 0.78
        }
        
        avg_difficulty = np.mean([
            difficulty_map.get(subj, 0.70) for subj in subjects
        ]) if subjects else 0.70
        
        return [subject_count, semester_factor, load_intensity, avg_difficulty]
    
    def _extract_engagement_features(self, attendance: List[float], 
                                      marks_history: List[Dict]) -> List[float]:
        """
        Cross-domain engagement indicators
        """
        # Attendance-performance correlation
        if len(attendance) >= 3 and marks_history:
            # Simplified correlation proxy
            recent_attendance = np.mean(attendance[-3:])
            
            all_recent_marks = []
            for subject_data in marks_history:
                marks = subject_data.get('marks', [])
                if marks:
                    all_recent_marks.append(marks[-1])
            
            recent_marks = np.mean(all_recent_marks) if all_recent_marks else 0
            
            engagement_score = (recent_attendance / 100.0) * (recent_marks / 20.0)
        else:
            engagement_score = 0.5
        
        # Data completeness (proxy for student engagement)
        data_completeness = min(len(attendance) / 10.0, 1.0)
        
        return [engagement_score, data_completeness]
    
    def get_feature_names(self) -> List[str]:
        """Return feature names for interpretability"""
        return [
            # Attendance features (6)
            'attendance_current', 'attendance_trend', 'attendance_volatility',
            'attendance_decline', 'decline_ratio', 'min_attendance',
            
            # Marks features (8)
            'marks_trend', 'marks_volatility', 'avg_performance', 'recent_performance',
            'declining_subjects_ratio', 'performance_range', 'weak_subjects_ratio', 'subject_count_marks',
            
            # Load features (4)
            'subject_count', 'semester_factor', 'load_intensity', 'avg_difficulty',
            
            # Historical features (2)
            'previous_failures', 'failure_rate',
            
            # Engagement features (2)
            'engagement_score', 'data_completeness'
        ]
    
    def get_feature_count(self) -> int:
        """Total number of features"""
        return len(self.get_feature_names())
