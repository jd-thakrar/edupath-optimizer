"""
AI Explainability Layer using Gemini API
Translates model outputs into human-understandable insights
"""

import google.generativeai as genai
from typing import Dict, Any, List
import os
import json


class ExplainabilityEngine:
    """
    Uses Gemini to explain AI predictions in natural language
    Gemini does NOT make decisions - only explains them
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def explain_risk_prediction(self, student_name: str, 
                                 prediction: Dict[str, Any],
                                 feature_importance: Dict[str, float],
                                 student_context: Dict[str, Any]) -> str:
        """
        Generate natural language explanation of risk prediction
        
        Args:
            student_name: Student's name
            prediction: Risk prediction output
            feature_importance: Feature importance scores
            student_context: Additional context about student
        
        Returns:
            Human-readable explanation
        """
        if not self.model:
            return self._fallback_explanation(student_name, prediction)
        
        # Prepare context for Gemini
        prompt = f"""
You are an empathetic academic advisor explaining AI-generated risk predictions to a student.

Student: {student_name}
Failure Probability: {prediction['failure_probability']*100:.1f}%
Confidence: {prediction['confidence']*100:.1f}%
Risk Level: {prediction['risk_level']}

Student Context:
- Current Semester: {student_context.get('semester', 'N/A')}
- Subjects Enrolled: {len(student_context.get('current_subjects', []))}
- Recent Attendance Trend: {student_context.get('attendance_trend', 'stable')}
- Performance Trend: {student_context.get('performance_trend', 'stable')}

Top Contributing Factors (from ML model):
{json.dumps(feature_importance, indent=2)}

Task:
1. Explain the risk prediction in clear, supportive language
2. Highlight the KEY factors contributing to this prediction
3. Explain what the confidence score means
4. DO NOT recommend actions (that's handled separately)
5. Focus on temporal patterns and trends, not just current values
6. Keep tone professional but encouraging
7. Limit to 150 words

Generate explanation:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_explanation(student_name, prediction)
    
    def explain_counterfactual(self, intervention: Dict[str, Any],
                                student_context: Dict[str, Any]) -> str:
        """
        Explain why a specific intervention is recommended
        """
        if not self.model:
            return self._fallback_counterfactual_explanation(intervention)
        
        prompt = f"""
You are an academic advisor explaining an AI-recommended intervention to a student.

Recommended Action: {intervention['action']}
Description: {intervention['description']}

Impact:
- Current Risk: {intervention['current_risk']*100:.1f}%
- Predicted Risk After Action: {intervention['predicted_risk']*100:.1f}%
- Risk Reduction: {intervention['risk_reduction_percent']}%

Effort Level: {intervention['effort_level']}/5
Effectiveness Score: {intervention['effectiveness_score']:.2f}

Student Context:
- Semester: {student_context.get('semester', 'N/A')}
- Current Subjects: {', '.join(student_context.get('current_subjects', []))}

Task:
1. Explain WHY this intervention is effective for THIS student
2. Make it actionable and specific
3. Explain the trade-off between effort and impact
4. Be encouraging and realistic
5. Limit to 120 words

Generate explanation:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_counterfactual_explanation(intervention)
    
    def explain_uncertainty(self, prediction: Dict[str, Any],
                             data_completeness: float) -> str:
        """
        Explain prediction uncertainty and confidence bounds
        """
        if not self.model:
            return self._fallback_uncertainty_explanation(prediction, data_completeness)
        
        prompt = f"""
You are explaining AI prediction uncertainty to a student.

Prediction Confidence: {prediction['confidence']*100:.1f}%
Data Completeness: {data_completeness*100:.1f}%
Risk Level: {prediction['risk_level']}

Task:
Explain in simple terms:
1. What does the confidence score mean?
2. Why might the prediction have uncertainty?
3. What would improve prediction accuracy?
4. Should the student trust this prediction?

Keep it under 100 words, use simple language.

Generate explanation:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_uncertainty_explanation(prediction, data_completeness)
    
    def explain_prerequisite_risk(self, course: str, 
                                    propagated_risks: Dict[str, float]) -> str:
        """
        Explain how failure in one course affects future courses
        """
        if not self.model or not propagated_risks:
            return self._fallback_prerequisite_explanation(course, propagated_risks)
        
        affected_courses = [
            f"{c}: {r*100:.1f}% risk" 
            for c, r in sorted(propagated_risks.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        prompt = f"""
You are explaining prerequisite dependencies to a student.

Current Course at Risk: {course}

This affects future courses:
{chr(10).join(affected_courses)}

Task:
1. Explain how struggling in {course} impacts future courses
2. Explain the concept of prerequisite dependencies
3. Emphasize the importance of addressing this early
4. Keep it under 100 words

Generate explanation:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_prerequisite_explanation(course, propagated_risks)
    
    def generate_personalized_summary(self, student_name: str,
                                       risk_assessment: Dict[str, Any],
                                       recommendations: List[Dict[str, Any]]) -> str:
        """
        Generate comprehensive personalized summary
        """
        if not self.model:
            return self._fallback_summary(student_name, risk_assessment, recommendations)
        
        prompt = f"""
You are an academic advisor writing a personalized report.

Student: {student_name}
Overall Risk: {risk_assessment.get('failure_probability', 0)*100:.1f}%

Top Recommendations:
{json.dumps([r['action'] for r in recommendations[:3]], indent=2)}

Task:
Write a 200-word personalized message that:
1. Acknowledges their current academic standing
2. Explains the risk level without alarming them
3. Highlights their potential for improvement
4. Frames recommendations as opportunities
5. Ends with encouragement

Tone: Professional, empathetic, motivating

Generate summary:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_summary(student_name, risk_assessment, recommendations)
    
    # Fallback methods when Gemini is unavailable
    
    def _fallback_explanation(self, student_name: str, prediction: Dict) -> str:
        risk_pct = prediction['failure_probability'] * 100
        conf_pct = prediction['confidence'] * 100
        
        return f"""Based on analysis of your academic patterns, your current failure risk is estimated at {risk_pct:.1f}% with {conf_pct:.1f}% confidence. This prediction considers your attendance trends, performance trajectory, and historical patterns rather than just current values. The model identified temporal trends in your academic engagement as key factors. {f"The {prediction['risk_level']} risk level suggests immediate attention is needed." if prediction['risk_level'] == 'high' else "Early intervention can significantly improve outcomes."}"""
    
    def _fallback_counterfactual_explanation(self, intervention: Dict) -> str:
        return f"""This intervention is recommended because it offers the highest risk-reduction-to-effort ratio ({intervention['effectiveness_score']:.2f}). By {intervention['description'].lower()}, you can reduce your failure risk from {intervention['current_risk']*100:.1f}% to {intervention['predicted_risk']*100:.1f}% - a {intervention['risk_reduction_percent']:.1f}% improvement. The effort level is rated {intervention['effort_level']}/5, making this a practical and impactful step."""
    
    def _fallback_uncertainty_explanation(self, prediction: Dict, completeness: float) -> str:
        return f"""The confidence score of {prediction['confidence']*100:.1f}% indicates how certain the model is about this prediction. With {completeness*100:.1f}% data completeness, the prediction is based on available patterns. Higher confidence means the model sees clear trends. More consistent data over time will improve prediction accuracy."""
    
    def _fallback_prerequisite_explanation(self, course: str, risks: Dict) -> str:
        if not risks:
            return f"No significant prerequisite dependencies detected for {course}."
        
        top_affected = sorted(risks.items(), key=lambda x: x[1], reverse=True)[:3]
        courses_str = ", ".join([c for c, _ in top_affected])
        
        return f"""Struggling in {course} has cascading effects on future courses: {courses_str}. These courses build on {course} as a foundation. Addressing challenges in {course} now prevents compounded difficulties later. Prerequisite mastery is critical for long-term success."""
    
    def _fallback_summary(self, student_name: str, risk: Dict, recs: List) -> str:
        return f"""{student_name}, based on comprehensive analysis of your academic journey, we've identified opportunities for improvement. Your current trajectory shows a {risk.get('failure_probability', 0)*100:.1f}% failure probability, but this is highly improvable through targeted interventions. The recommendations provided are data-driven and personalized to your specific patterns. Small, consistent improvements in the suggested areas can significantly enhance your academic outcomes. You have the potential to succeed - these insights are meant to empower you with actionable next steps."""
