"""
Cross-Cultural Empathy Modeling
Translates emotional content between cultural contexts through musical adaptation
"""

import numpy as np
from typing import Dict, List, Tuple

class CrossCulturalEmpathyEngine:
    """
    Advanced system for modeling cross-cultural empathy through music translation.
    Enables emotional content to be adapted between different cultural contexts.
    """
    
    # Cultural emotional archetypes
    CULTURAL_ARCHETYPES = {
        'western': {
            'emotional_range': {'joy': (0.7, 1.0), 'sadness': (0.0, 0.3), 'anger': (0.6, 0.9), 'peace': (0.4, 0.6)},
            'expression_style': 'direct',
            'harmonic_complexity': 'moderate',
            'rhythmic_structure': 'regular'
        },
        'eastern': {
            'emotional_range': {'joy': (0.5, 0.8), 'sadness': (0.2, 0.5), 'anger': (0.3, 0.6), 'peace': (0.6, 0.9)},
            'expression_style': 'subtle',
            'harmonic_complexity': 'high',
            'rhythmic_structure': 'fluid'
        },
        'african': {
            'emotional_range': {'joy': (0.6, 1.0), 'sadness': (0.1, 0.4), 'anger': (0.5, 0.8), 'peace': (0.3, 0.6)},
            'expression_style': 'communal',
            'harmonic_complexity': 'polyphonic',
            'rhythmic_structure': 'complex'
        },
        'latin': {
            'emotional_range': {'joy': (0.7, 1.0), 'sadness': (0.2, 0.5), 'anger': (0.6, 0.9), 'peace': (0.3, 0.5)},
            'expression_style': 'passionate',
            'harmonic_complexity': 'moderate',
            'rhythmic_structure': 'syncopated'
        }
    }
    
    # Empathy bridge mappings (how emotions translate between cultures)
    EMPATHY_BRIDGES = {
        ('western', 'eastern'): {
            'direct_joy': 'subtle_joy',
            'direct_sadness': 'melancholy',
            'direct_anger': 'restrained_tension',
            'direct_peace': 'inner_peace'
        },
        ('western', 'african'): {
            'direct_joy': 'communal_celebration',
            'direct_sadness': 'collective_mourning',
            'direct_anger': 'rhythmic_protest',
            'direct_peace': 'community_harmony'
        },
        ('western', 'latin'): {
            'direct_joy': 'passionate_exuberance',
            'direct_sadness': 'dramatic_melancholy',
            'direct_anger': 'fiery_passion',
            'direct_peace': 'romantic_tranquility'
        },
        ('eastern', 'western'): {
            'subtle_joy': 'gentle_happiness',
            'melancholy': 'reflective_sadness',
            'restrained_tension': 'controlled_anger',
            'inner_peace': 'spiritual_peace'
        }
    }
    
    def __init__(self):
        self.empathy_history = []
        self.translation_accuracy = {}
    
    def analyze_cultural_emotional_profile(self, analysis_result: Dict) -> Dict:
        """
        Analyze the emotional profile within a cultural context.
        
        Args:
            analysis_result: Text analysis results
            
        Returns:
            Cultural emotional profile
        """
        cultural_context = analysis_result.get('cultural_context', 'western')
        sentiment = analysis_result.get('sentiment', 0.5)
        arousal = analysis_result.get('arousal', 0.5)
        complexity = analysis_result.get('complexity', 0.5)
        
        archetype = self.CULTURAL_ARCHETYPES.get(cultural_context, self.CULTURAL_ARCHETYPES['western'])
        
        # Determine primary emotion based on sentiment and arousal
        if sentiment > 0.7 and arousal > 0.6:
            primary_emotion = 'joy'
        elif sentiment < 0.3 and arousal < 0.4:
            primary_emotion = 'sadness'
        elif sentiment < 0.5 and arousal > 0.7:
            primary_emotion = 'anger'
        else:
            primary_emotion = 'peace'
        
        # Check if emotion fits cultural archetype
        emotion_range = archetype['emotional_range'].get(primary_emotion, (0.0, 1.0))
        fits_archetype = emotion_range[0] <= sentiment <= emotion_range[1]
        
        profile = {
            'cultural_context': cultural_context,
            'primary_emotion': primary_emotion,
            'sentiment': sentiment,
            'arousal': arousal,
            'complexity': complexity,
            'expression_style': archetype['expression_style'],
            'harmonic_complexity': archetype['harmonic_complexity'],
            'rhythmic_structure': archetype['rhythmic_structure'],
            'fits_archetype': fits_archetype,
            'cultural_alignment_score': self._calculate_cultural_alignment(sentiment, arousal, cultural_context)
        }
        
        return profile
    
    def _calculate_cultural_alignment(self, sentiment: float, arousal: float, culture: str) -> float:
        """Calculate how well the emotional state aligns with cultural norms."""
        archetype = self.CULTURAL_ARCHETYPES.get(culture, self.CULTURAL_ARCHETYPES['western'])
        
        # Determine emotion
        if sentiment > 0.7 and arousal > 0.6:
            emotion = 'joy'
        elif sentiment < 0.3 and arousal < 0.4:
            emotion = 'sadness'
        elif sentiment < 0.5 and arousal > 0.7:
            emotion = 'anger'
        else:
            emotion = 'peace'
        
        emotion_range = archetype['emotional_range'].get(emotion, (0.0, 1.0))
        
        # Calculate alignment score
        if emotion_range[0] <= sentiment <= emotion_range[1]:
            return 1.0
        else:
            distance = min(abs(sentiment - emotion_range[0]), abs(sentiment - emotion_range[1]))
            return max(0.0, 1.0 - distance)
    
    def translate_emotional_content(self, source_profile: Dict, target_culture: str) -> Dict:
        """
        Translate emotional content from source culture to target culture.
        
        Args:
            source_profile: Source cultural emotional profile
            target_culture: Target cultural context
            
        Returns:
            Translated emotional profile for target culture
        """
        source_culture = source_profile['cultural_context']
        primary_emotion = source_profile['primary_emotion']
        
        # Get empathy bridge
        bridge_key = (source_culture, target_culture)
        if bridge_key not in self.EMPATHY_BRIDGES:
            # Reverse bridge
            bridge_key = (target_culture, source_culture)
        
        if bridge_key in self.EMPATHY_BRIDGES:
            bridge = self.EMPATHY_BRIDGES[bridge_key]
            source_emotion_key = f"{source_profile['expression_style']}_{primary_emotion}"
            
            if source_emotion_key in bridge:
                translated_emotion = bridge[source_emotion_key]
            else:
                translated_emotion = primary_emotion
        else:
            translated_emotion = primary_emotion
        
        # Adapt emotional parameters to target culture
        target_archetype = self.CULTURAL_ARCHETYPES.get(target_culture, self.CULTURAL_ARCHETYPES['western'])
        target_emotion_range = target_archetype['emotional_range'].get(translated_emotion, (0.0, 1.0))
        
        # Map sentiment to target emotional range
        original_sentiment = source_profile['sentiment']
        target_sentiment = self._map_to_range(original_sentiment, target_emotion_range)
        
        # Adjust arousal based on target cultural expression style
        target_arousal = self._adjust_arousal_for_culture(source_profile['arousal'], target_culture)
        
        # Adapt complexity
        target_complexity = self._adapt_complexity(source_profile['complexity'], target_culture)
        
        translated_profile = {
            'source_culture': source_culture,
            'target_culture': target_culture,
            'original_emotion': primary_emotion,
            'translated_emotion': translated_emotion,
            'original_sentiment': original_sentiment,
            'translated_sentiment': target_sentiment,
            'original_arousal': source_profile['arousal'],
            'translated_arousal': target_arousal,
            'original_complexity': source_profile['complexity'],
            'translated_complexity': target_complexity,
            'expression_style': target_archetype['expression_style'],
            'harmonic_complexity': target_archetype['harmonic_complexity'],
            'rhythmic_structure': target_archetype['rhythmic_structure'],
            'empathy_bridge_used': bridge_key in self.EMPATHY_BRIDGES
        }
        
        # Record translation for learning
        self.empathy_history.append(translated_profile)
        
        return translated_profile
    
    def _map_to_range(self, value: float, target_range: Tuple[float, float]) -> float:
        """Map a value to a target range while preserving relative position."""
        min_val, max_val = target_range
        return min_val + (value * (max_val - min_val))
    
    def _adjust_arousal_for_culture(self, arousal: float, target_culture: str) -> float:
        """Adjust arousal level based on target cultural expression style."""
        archetype = self.CULTURAL_ARCHETYPES.get(target_culture, self.CULTURAL_ARCHETYPES['western'])
        
        if archetype['expression_style'] == 'subtle':
            return arousal * 0.7  # Dampen arousal for subtle cultures
        elif archetype['expression_style'] == 'passionate':
            return min(1.0, arousal * 1.3)  # Amplify arousal for passionate cultures
        elif archetype['expression_style'] == 'communal':
            return arousal * 0.9  # Moderate arousal for communal cultures
        else:
            return arousal  # Keep original for direct cultures
    
    def _adapt_complexity(self, complexity: float, target_culture: str) -> float:
        """Adapt complexity based on target cultural harmonic complexity."""
        archetype = self.CULTURAL_ARCHETYPES.get(target_culture, self.CULTURAL_ARCHETYPES['western'])
        
        if archetype['harmonic_complexity'] == 'high':
            return min(1.0, complexity + 0.2)
        elif archetype['harmonic_complexity'] == 'polyphonic':
            return min(1.0, complexity + 0.3)
        elif archetype['harmonic_complexity'] == 'moderate':
            return complexity
        else:
            return max(0.0, complexity - 0.1)
    
    def generate_empathy_metrics(self) -> Dict:
        """
        Generate metrics about cross-cultural empathy performance.
        
        Returns:
            Dictionary of empathy metrics
        """
        if not self.empathy_history:
            return {'message': 'No empathy translations performed yet'}
        
        total_translations = len(self.empathy_history)
        successful_bridges = sum(1 for t in self.empathy_history if t['empathy_bridge_used'])
        
        # Calculate average sentiment preservation
        sentiment_changes = [abs(t['original_sentiment'] - t['translated_sentiment']) 
                           for t in self.empathy_history]
        avg_sentiment_change = np.mean(sentiment_changes) if sentiment_changes else 0.0
        
        # Cultural distribution
        culture_pairs = {}
        for t in self.empathy_history:
            pair = f"{t['source_culture']}->{t['target_culture']}"
            culture_pairs[pair] = culture_pairs.get(pair, 0) + 1
        
        return {
            'total_translations': total_translations,
            'successful_empathy_bridges': successful_bridges,
            'bridge_success_rate': successful_bridges / total_translations if total_translations > 0 else 0.0,
            'average_sentiment_change': avg_sentiment_change,
            'cultural_translation_distribution': culture_pairs,
            'empathy_engine_accuracy': 1.0 - avg_sentiment_change
        }
    
    def suggest_cultural_adaptations(self, analysis_result: Dict, target_cultures: List[str]) -> Dict:
        """
        Suggest how to adapt content for multiple target cultures.
        
        Args:
            analysis_result: Original text analysis
            target_cultures: List of target cultures to adapt for
            
        Returns:
            Dictionary of adaptation suggestions
        """
        source_profile = self.analyze_cultural_emotional_profile(analysis_result)
        
        suggestions = {}
        for target_culture in target_cultures:
            if target_culture == source_profile['cultural_context']:
                suggestions[target_culture] = {'message': 'Same culture, no adaptation needed'}
            else:
                translated = self.translate_emotional_content(source_profile, target_culture)
                suggestions[target_culture] = {
                    'translated_emotion': translated['translated_emotion'],
                    'sentiment_adjustment': translated['translated_sentiment'] - translated['original_sentiment'],
                    'arousal_adjustment': translated['translated_arousal'] - translated['original_arousal'],
                    'complexity_adjustment': translated['translated_complexity'] - translated['original_complexity'],
                    'expression_style_change': f"{source_profile['expression_style']} -> {translated['expression_style']}",
                    'rhythmic_change': f"{source_profile['rhythmic_structure']} -> {translated['rhythmic_structure']}"
                }
        
        return suggestions
