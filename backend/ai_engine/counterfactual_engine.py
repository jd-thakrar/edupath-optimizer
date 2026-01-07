"""
Counterfactual Simulation Engine
Answers: "What minimal action reduces failure probability the most?"
This is the CORE intelligence component
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from copy import deepcopy


class CounterfactualEngine:
    """
    Simulates alternative futures to find minimal interventions
    Uses gradient-based reasoning and what-if analysis
    """
    
    def __init__(self, feature_engineer, risk_predictor):
        self.feature_engineer = feature_engineer
        self.risk_predictor = risk_predictor
        
        # Define intervention scenarios
        self.interventions = [
            {
                'name': 'Improve Attendance',
                'description': 'Attend {delta} more classes consistently',
                'feature_indices': [0, 1],  # attendance_current, attendance_trend
                'delta_range': [0.05, 0.10, 0.15, 0.20],  # 5%, 10%, 15%, 20%
                'effort_cost': 2
            },
            {
                'name': 'Boost Internal Marks',
                'description': 'Improve test scores by {delta} marks on average',
                'feature_indices': [8, 9],  # marks_trend, avg_performance
                'delta_range': [0.10, 0.20, 0.30, 0.40],  # normalized improvements
                'effort_cost': 3
            },
            {
                'name': 'Stabilize Performance',
                'description': 'Reduce performance volatility and maintain consistency',
                'feature_indices': [7, 13],  # marks_volatility, performance_range
                'delta_range': [-0.10, -0.20, -0.30],  # reduce volatility
                'effort_cost': 2
            },
            {
                'name': 'Increase Engagement',
                'description': 'Improve overall academic engagement',
                'feature_indices': [20],  # engagement_score
                'delta_range': [0.10, 0.20, 0.30],
                'effort_cost': 2
            }
        ]
    
    def simulate_interventions(self, student_data: Dict[str, Any], 
                               current_risk: float) -> List[Dict[str, Any]]:
        """
        Simulate all possible interventions and rank by effectiveness
        
        Args:
            student_data: Current student data
            current_risk: Current failure probability
        
        Returns:
            List of interventions ranked by risk reduction per effort
        """
        # Extract current features
        current_features = self.feature_engineer.extract_features(student_data)
        
        # Simulate each intervention
        results = []
        
        for intervention in self.interventions:
            best_scenario = self._simulate_intervention(
                current_features,
                intervention,
                current_risk
            )
            
            if best_scenario:
                results.append(best_scenario)
        
        # Rank by effectiveness (risk reduction per effort unit)
        results.sort(key=lambda x: x['effectiveness_score'], reverse=True)
        
        return results[:3]  # Return top 3 recommendations
    
    def _simulate_intervention(self, current_features: np.ndarray,
                                intervention: Dict, current_risk: float) -> Dict:
        """
        Simulate a specific intervention type with different intensities
        """
        best_result = None
        best_effectiveness = -1
        
        for delta in intervention['delta_range']:
            # Create modified features
            modified_features = current_features.copy()
            
            # Apply intervention
            for idx in intervention['feature_indices']:
                if idx < len(modified_features):
                    modified_features[idx] += delta
                    # Clip to valid range
                    modified_features[idx] = np.clip(modified_features[idx], 0.0, 1.0)
            
            # Predict new risk
            prediction = self.risk_predictor.predict(modified_features)
            new_risk = prediction['failure_probability']
            
            # Calculate risk reduction
            risk_reduction = current_risk - new_risk
            
            # Skip if no improvement
            if risk_reduction <= 0:
                continue
            
            # Calculate effectiveness (risk reduction per effort unit)
            effectiveness = risk_reduction / intervention['effort_cost']
            
            if effectiveness > best_effectiveness:
                best_effectiveness = effectiveness
                best_result = {
                    'action': intervention['name'],
                    'description': intervention['description'].format(
                        delta=self._format_delta(delta, intervention['name'])
                    ),
                    'current_risk': round(current_risk, 4),
                    'predicted_risk': round(new_risk, 4),
                    'risk_reduction': round(risk_reduction, 4),
                    'risk_reduction_percent': round(risk_reduction * 100, 1),
                    'effort_level': intervention['effort_cost'],
                    'effectiveness_score': round(effectiveness, 4),
                    'confidence': prediction['confidence']
                }
        
        return best_result
    
    def _format_delta(self, delta: float, action_name: str) -> str:
        """Format delta value based on intervention type"""
        if 'Attendance' in action_name:
            return f"{int(abs(delta) * 100)}%"
        elif 'Marks' in action_name:
            return f"{int(abs(delta) * 20)}"  # denormalize
        elif 'Engagement' in action_name:
            return f"{int(abs(delta) * 100)}%"
        else:
            return f"{abs(delta):.2f}"
    
    def explain_recommendation(self, intervention: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of recommendation
        """
        risk_change = f"{intervention['current_risk']*100:.1f}% → {intervention['predicted_risk']*100:.1f}%"
        
        explanation = f"""
**Recommended Action: {intervention['action']}**

{intervention['description']}

**Impact:**
- Current Failure Risk: {intervention['current_risk']*100:.1f}%
- Predicted Risk After Action: {intervention['predicted_risk']*100:.1f}%
- Risk Reduction: {intervention['risk_reduction_percent']}%

**Effort Required:** {'⭐' * intervention['effort_level']} ({intervention['effort_level']}/5)

**Effectiveness Score:** {intervention['effectiveness_score']:.2f} (higher is better)

This intervention offers the best risk-reduction-to-effort ratio based on your current academic trajectory.
"""
        return explanation.strip()
    
    def simulate_combined_interventions(self, student_data: Dict[str, Any],
                                         interventions: List[str]) -> Dict[str, Any]:
        """
        Simulate effect of multiple interventions combined
        Used for advanced "what-if" scenarios
        """
        current_features = self.feature_engineer.extract_features(student_data)
        current_prediction = self.risk_predictor.predict(current_features)
        
        # Apply all interventions
        modified_features = current_features.copy()
        total_effort = 0
        
        for intervention_name in interventions:
            intervention = next((i for i in self.interventions if i['name'] == intervention_name), None)
            if not intervention:
                continue
            
            # Apply moderate delta
            delta = intervention['delta_range'][1] if len(intervention['delta_range']) > 1 else intervention['delta_range'][0]
            
            for idx in intervention['feature_indices']:
                if idx < len(modified_features):
                    modified_features[idx] += delta
                    modified_features[idx] = np.clip(modified_features[idx], 0.0, 1.0)
            
            total_effort += intervention['effort_cost']
        
        # Predict combined effect
        new_prediction = self.risk_predictor.predict(modified_features)
        
        return {
            'original_risk': current_prediction['failure_probability'],
            'combined_risk': new_prediction['failure_probability'],
            'total_risk_reduction': current_prediction['failure_probability'] - new_prediction['failure_probability'],
            'total_effort': total_effort,
            'interventions_applied': interventions
        }
    
    def find_minimal_safe_path(self, student_data: Dict[str, Any], 
                                target_risk: float = 0.3) -> Dict[str, Any]:
        """
        Find the minimum intervention needed to reach target safety threshold
        Uses iterative simulation
        """
        current_features = self.feature_engineer.extract_features(student_data)
        current_prediction = self.risk_predictor.predict(current_features)
        current_risk = current_prediction['failure_probability']
        
        if current_risk <= target_risk:
            return {
                'status': 'safe',
                'message': 'Student is already below target risk threshold',
                'current_risk': current_risk,
                'target_risk': target_risk
            }
        
        # Try single interventions first
        interventions = self.simulate_interventions(student_data, current_risk)
        
        for intervention in interventions:
            if intervention['predicted_risk'] <= target_risk:
                return {
                    'status': 'solution_found',
                    'path': [intervention],
                    'final_risk': intervention['predicted_risk'],
                    'total_effort': intervention['effort_level']
                }
        
        # If single intervention not enough, try combinations
        # For MVP, return best single intervention with note
        if interventions:
            best = interventions[0]
            return {
                'status': 'partial_solution',
                'path': [best],
                'final_risk': best['predicted_risk'],
                'total_effort': best['effort_level'],
                'note': 'Multiple interventions may be needed to reach target safety level'
            }
        
        return {
            'status': 'no_solution',
            'message': 'Unable to find viable intervention path',
            'current_risk': current_risk
        }
