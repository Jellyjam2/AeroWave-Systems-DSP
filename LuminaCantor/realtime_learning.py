"""
Real-Time Learning System
Learns from user feedback to improve musical generation quality
"""

import json
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

class RealTimeLearningEngine:
    """
    Machine learning system that improves from user feedback in real-time.
    """
    
    def __init__(self, feedback_file: str = "user_feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_history = []
        self.user_preferences = defaultdict(dict)
        self.model_weights = {
            'sentiment_importance': 0.25,
            'arousal_importance': 0.25,
            'complexity_importance': 0.20,
            'cultural_importance': 0.15,
            'sat_importance': 0.15
        }
        self.load_feedback()
    
    def load_feedback(self):
        """Load existing feedback from file."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = data.get('feedback_history', [])
                    self.user_preferences = defaultdict(dict, data.get('user_preferences', {}))
                    self.model_weights = data.get('model_weights', self.model_weights)
                print(f"  [LEARNING]: Loaded {len(self.feedback_history)} feedback records")
            except Exception as e:
                print(f"  [LEARNING]: Error loading feedback: {e}")
    
    def save_feedback(self):
        """Save feedback to file."""
        try:
            data = {
                'feedback_history': self.feedback_history,
                'user_preferences': dict(self.user_preferences),
                'model_weights': self.model_weights
            }
            with open(self.feedback_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"  [LEARNING]: Saved {len(self.feedback_history)} feedback records")
        except Exception as e:
            print(f"  [LEARNING]: Error saving feedback: {e}")
    
    def record_feedback(self, user_id: str, analysis_result: Dict, feedback_data: Dict):
        """
        Record user feedback for a generated piece.
        
        Args:
            user_id: Unique user identifier
            analysis_result: The analysis that generated the music
            feedback_data: User feedback (rating, comments, etc.)
        """
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'input_text': feedback_data.get('input_text', ''),
            'cultural_context': analysis_result.get('cultural_context', 'western'),
            'sentiment': analysis_result.get('sentiment', 0.5),
            'arousal': analysis_result.get('arousal', 0.5),
            'complexity': analysis_result.get('complexity', 0.5),
            'rating': feedback_data.get('rating', 0),  # 1-5 scale
            'liked_aspects': feedback_data.get('liked_aspects', []),
            'disliked_aspects': feedback_data.get('disliked_aspects', []),
            'comments': feedback_data.get('comments', ''),
            'sat_used': analysis_result.get('sat_recommendations') is not None
        }
        
        self.feedback_history.append(feedback_record)
        
        # Update user preferences
        self._update_user_preferences(user_id, feedback_record)
        
        # Update model weights based on feedback
        self._update_model_weights(feedback_record)
        
        # Save feedback
        self.save_feedback()
        
        print(f"  [LEARNING]: Recorded feedback from user {user_id} (rating: {feedback_record['rating']}/5)")
        
        return feedback_record
    
    def _update_user_preferences(self, user_id: str, feedback_record: Dict):
        """Update individual user preferences based on feedback."""
        user_prefs = self.user_preferences[user_id]
        
        # Track preferred cultural contexts
        culture = feedback_record['cultural_context']
        if culture not in user_prefs:
            user_prefs[culture] = {'count': 0, 'total_rating': 0}
        
        user_prefs[culture]['count'] += 1
        user_prefs[culture]['total_rating'] += feedback_record['rating']
        
        # Track preferred sentiment ranges
        sentiment = feedback_record['sentiment']
        if 'preferred_sentiment_range' not in user_prefs:
            user_prefs['preferred_sentiment_range'] = []
        user_prefs['preferred_sentiment_range'].append((sentiment, feedback_record['rating']))
        
        # Track preferred arousal levels
        arousal = feedback_record['arousal']
        if 'preferred_arousal_range' not in user_prefs:
            user_prefs['preferred_arousal_range'] = []
        user_prefs['preferred_aroural_range'] = user_prefs['preferred_arousal_range']  # Fix typo
        user_prefs['preferred_arousal_range'].append((arousal, feedback_record['rating']))
    
    def _update_model_weights(self, feedback_record: Dict):
        """Update model weights based on aggregated feedback."""
        rating = feedback_record['rating']
        
        # If rating is high, increase weight of successful factors
        if rating >= 4:
            if feedback_record['sat_used']:
                self.model_weights['sat_importance'] = min(1.0, self.model_weights['sat_importance'] + 0.01)
            
            # Adjust based on cultural alignment
            if feedback_record['cultural_context'] in feedback_record.get('liked_aspects', []):
                self.model_weights['cultural_importance'] = min(1.0, self.model_weights['cultural_importance'] + 0.01)
        
        # If rating is low, decrease weight of unsuccessful factors
        elif rating <= 2:
            if feedback_record['sat_used']:
                self.model_weights['sat_importance'] = max(0.0, self.model_weights['sat_importance'] - 0.01)
            
            if feedback_record['cultural_context'] in feedback_record.get('disliked_aspects', []):
                self.model_weights['cultural_importance'] = max(0.0, self.model_weights['cultural_importance'] - 0.01)
        
        # Normalize weights
        total_weight = sum(self.model_weights.values())
        if total_weight > 0:
            for key in self.model_weights:
                self.model_weights[key] /= total_weight
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get learned preferences for a specific user."""
        user_prefs = self.user_preferences.get(user_id, {})
        
        if not user_prefs:
            return {'message': 'No preferences learned yet for this user'}
        
        # Calculate average ratings per culture
        culture_preferences = {}
        for culture, data in user_prefs.items():
            if isinstance(data, dict) and 'count' in data:
                avg_rating = data['total_rating'] / data['count'] if data['count'] > 0 else 0
                culture_preferences[culture] = {
                    'count': data['count'],
                    'average_rating': avg_rating
                }
        
        # Find preferred sentiment range
        sentiment_data = user_prefs.get('preferred_sentiment_range', [])
        if sentiment_data:
            high_rated_sentiments = [s for s, r in sentiment_data if r >= 4]
            if high_rated_sentiments:
                preferred_sentiment = {
                    'min': min(high_rated_sentiments),
                    'max': max(high_rated_sentiments),
                    'avg': np.mean(high_rated_sentiments)
                }
            else:
                preferred_sentiment = None
        else:
            preferred_sentiment = None
        
        return {
            'cultural_preferences': culture_preferences,
            'preferred_sentiment_range': preferred_sentiment,
            'total_feedback_records': len([f for f in self.feedback_history if f['user_id'] == user_id])
        }
    
    def apply_user_preferences(self, user_id: str, analysis_result: Dict) -> Dict:
        """
        Apply learned user preferences to analysis results.
        
        Args:
            user_id: User identifier
            analysis_result: Original analysis results
            
        Returns:
            Modified analysis results with user preferences applied
        """
        user_prefs = self.get_user_preferences(user_id)
        
        if 'message' in user_prefs:
            # No preferences learned yet
            return analysis_result
        
        modified_result = analysis_result.copy()
        
        # Apply cultural preference if available
        cultural_prefs = user_prefs.get('cultural_preferences', {})
        if cultural_prefs:
            best_culture = max(cultural_prefs, key=lambda x: cultural_prefs[x]['average_rating'])
            if cultural_prefs[best_culture]['average_rating'] >= 4.0:
                modified_result['cultural_context'] = best_culture
                print(f"  [LEARNING]: Applied user preference for {best_culture} culture")
        
        # Apply sentiment preference if available
        sentiment_pref = user_prefs.get('preferred_sentiment_range')
        if sentiment_pref:
            current_sentiment = analysis_result.get('sentiment', 0.5)
            # Move towards preferred range
            if current_sentiment < sentiment_pref['min']:
                modified_result['sentiment'] = (current_sentiment + sentiment_pref['min']) / 2
            elif current_sentiment > sentiment_pref['max']:
                modified_result['sentiment'] = (current_sentiment + sentiment_pref['max']) / 2
            print(f"  [LEARNING]: Adjusted sentiment from {current_sentiment:.2f} to {modified_result['sentiment']:.2f}")
        
        return modified_result
    
    def get_learning_metrics(self) -> Dict:
        """Get overall learning system metrics."""
        if not self.feedback_history:
            return {'message': 'No feedback data available'}
        
        total_feedback = len(self.feedback_history)
        average_rating = np.mean([f['rating'] for f in self.feedback_history])
        
        # Rating distribution
        rating_distribution = defaultdict(int)
        for f in self.feedback_history:
            rating_distribution[f['rating']] += 1
        
        # Cultural preference distribution
        culture_distribution = defaultdict(int)
        for f in self.feedback_history:
            culture_distribution[f['cultural_context']] += 1
        
        # SAT solver effectiveness
        sat_feedback = [f for f in self.feedback_history if f['sat_used']]
        sat_avg_rating = np.mean([f['rating'] for f in sat_feedback]) if sat_feedback else 0
        non_sat_feedback = [f for f in self.feedback_history if not f['sat_used']]
        non_sat_avg_rating = np.mean([f['rating'] for f in non_sat_feedback]) if non_sat_feedback else 0
        
        return {
            'total_feedback_records': total_feedback,
            'average_rating': average_rating,
            'rating_distribution': dict(rating_distribution),
            'cultural_distribution': dict(culture_distribution),
            'sat_solver_effectiveness': {
                'sat_avg_rating': sat_avg_rating,
                'non_sat_avg_rating': non_sat_avg_rating,
                'improvement': sat_avg_rating - non_sat_avg_rating
            },
            'current_model_weights': self.model_weights,
            'unique_users': len(set(f['user_id'] for f in self.feedback_history))
        }
    
    def suggest_improvements(self) -> List[str]:
        """Suggest system improvements based on feedback analysis."""
        suggestions = []
        metrics = self.get_learning_metrics()
        
        if 'message' in metrics:
            return ['Collect more user feedback to generate improvement suggestions']
        
        # Check if SAT solver is helping
        sat_effectiveness = metrics.get('sat_solver_effectiveness', {})
        if sat_effectiveness.get('improvement', 0) < 0:
            suggestions.append("SAT solver may be degrading quality - consider adjusting constraints")
        elif sat_effectiveness.get('improvement', 0) > 0.5:
            suggestions.append("SAT solver is significantly improving quality - consider expanding its use")
        
        # Check cultural distribution
        culture_dist = metrics.get('cultural_distribution', {})
        if len(culture_dist) < 2:
            suggestions.append("Need more diverse cultural feedback to improve cross-cultural modeling")
        
        # Check average rating
        if metrics['average_rating'] < 3.0:
            suggestions.append("Overall quality is below target - review generation parameters")
        elif metrics['average_rating'] >= 4.0:
            suggestions.append("Quality is high - consider adding more advanced features")
        
        # Check model weights
        weights = metrics.get('current_model_weights', {})
        if weights.get('sat_importance', 0) < 0.1:
            suggestions.append("SAT solver weight is very low - may need constraint refinement")
        
        return suggestions if suggestions else ['System performing well - no major improvements needed']
