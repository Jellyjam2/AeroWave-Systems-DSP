# This module will convert SAT solutions into musical output.
from midiutil import MIDIFile
import os
import numpy as np

class AdvancedMusicGenerator:
    """
    Advanced music generator with multi-instrument orchestration capabilities.
    """
    
    def __init__(self):
        self.scale_patterns = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        self.chord_progressions = {
            'happy': [[0, 4, 7], [5, 9, 12], [3, 7, 10], [0, 4, 7]],  # I-V-vi-I
            'sad': [[0, 3, 7], [5, 8, 12], [3, 6, 10], [0, 3, 7]],    # i-vi-III-i
            'tense': [[0, 4, 7], [2, 6, 9], [5, 9, 12], [7, 11, 14]], # I-iii-V-vii
            'mysterious': [[0, 3, 6], [5, 8, 11], [7, 10, 13], [0, 3, 6]]  # i°-vi°-vii°-i°
        }
    
    def generate_midi(self, analysis_result, output_path="output.mid"):
        """
        Converts advanced text analysis into multi-track MIDI orchestration.
        
        Args:
            analysis_result: Dictionary containing emotional vectors, sentiment, rhythm patterns
            output_path: Path where the MIDI file will be saved
        """
        emotional_vector = analysis_result.get('emotional_vector', [])
        sentiment = analysis_result.get('sentiment', 0.5)
        arousal = analysis_result.get('arousal', 0.5)
        rhythm_pattern = analysis_result.get('rhythm_pattern', [])
        harmonic_progression = analysis_result.get('harmonic_progression', [])
        cultural_context = analysis_result.get('cultural_context', 'western')
        cultural_influence = analysis_result.get('cultural_influence', 0.0)
        sat_recommendations = analysis_result.get('sat_recommendations', None)
        
        print(f"  [MUSIC GENERATOR]: Generating orchestral arrangement...")
        print(f"  [MUSIC GENERATOR]: Sentiment: {sentiment:.2f}, Arousal: {arousal:.2f}")
        print(f"  [MUSIC GENERATOR]: Cultural Context: {cultural_context} (influence: {cultural_influence:.2f})")
        
        if sat_recommendations:
            print(f"  [MUSIC GENERATOR]: Applying SAT solver optimizations")
        
        # Create MIDIFile with multiple tracks
        num_tracks = 5  # Melody, Harmony, Bass, Drums, Pad
        midi = MIDIFile(num_tracks)
        
        # Track configuration with cultural instrument selection
        tracks = self._get_cultural_track_configuration(cultural_context)
        
        # Initialize tracks
        time = 0
        tempo = int(100 + (arousal * 60))  # Tempo based on arousal (100-160 BPM)
        
        for track_num, config in tracks.items():
            midi.addTrackName(track_num, time, config['name'])
            midi.addTempo(track_num, time, tempo)
            if track_num != 3:  # Drums don't need program change
                midi.addProgramChange(track_num, config['channel'], time, config['program'])
        
        # Select scale based on cultural context
        scale = self._get_cultural_scale(cultural_context, sentiment)
        
        # Generate melody track with cultural influence and SAT optimizations
        self._generate_melody(midi, 0, emotional_vector, rhythm_pattern, sentiment, scale, cultural_influence, sat_recommendations, time)
        
        # Generate harmony track
        self._generate_harmony(midi, 1, harmonic_progression, sentiment, scale, time)
        
        # Generate bass track
        self._generate_bass(midi, 2, emotional_vector, sentiment, scale, time)
        
        # Generate drum track with cultural patterns
        self._generate_drums(midi, 3, rhythm_pattern, arousal, cultural_context, time)
        
        # Generate pad track
        self._generate_pad(midi, 4, sentiment, scale, time)
        
        # Write to file
        with open(output_path, "wb") as output_file:
            midi.writeFile(output_file)
        
        print(f"  [MUSIC GENERATOR]: Orchestral MIDI saved to '{output_path}'")
        return output_path, None
    
    def _get_cultural_track_configuration(self, cultural_context: str) -> dict:
        """Return track configuration based on cultural context."""
        base_config = {
            0: {'name': 'Melody', 'channel': 0, 'program': 0},
            1: {'name': 'Harmony', 'channel': 1, 'program': 48},
            2: {'name': 'Bass', 'channel': 2, 'program': 33},
            3: {'name': 'Drums', 'channel': 9, 'program': 0},
            4: {'name': 'Pad', 'channel': 3, 'program': 89}
        }
        
        # Adjust instruments based on culture
        if cultural_context == 'eastern':
            base_config[0]['program'] = 24  # Nylon guitar (koto-like)
            base_config[1]['program'] = 45   # Pizzicato strings
        elif cultural_context == 'african':
            base_config[1]['program'] = 25   # Acoustic guitar
            base_config[4]['program'] = 78   # Whistle (percussion-like)
        elif cultural_context == 'latin':
            base_config[0]['program'] = 26   # Jazz guitar
            base_config[1]['program'] = 30   # Overdriven guitar
        
        return base_config
    
    def _get_cultural_scale(self, cultural_context: str, sentiment: float) -> list:
        """Return musical scale based on cultural context and sentiment."""
        if cultural_context == 'eastern':
            return self.scale_patterns['pentatonic']
        elif cultural_context == 'african':
            return self.scale_patterns['blues']
        elif cultural_context == 'latin':
            return self.scale_patterns['major'] if sentiment > 0.5 else self.scale_patterns['minor']
        else:  # western
            return self.scale_patterns['major'] if sentiment > 0.5 else self.scale_patterns['minor']
    
    def _generate_melody(self, midi, track_num, emotional_vector, rhythm_pattern, sentiment, scale, cultural_influence, sat_recommendations, start_time):
        """Generate melodic line based on emotional vector with cultural influence and SAT optimizations."""
        time = start_time
        base_note = 60 if sentiment > 0.5 else 57  # C major or A minor
        
        for i, score in enumerate(emotional_vector):
            # Select note from scale
            scale_degree = int(score * (len(scale) - 1))
            pitch = base_note + scale[scale_degree]
            
            # Apply SAT solver pitch adjustments if available
            if sat_recommendations and 'pitch_adjustments' in sat_recommendations:
                if i < len(sat_recommendations['pitch_adjustments']):
                    pitch += sat_recommendations['pitch_adjustments'][i]
            
            # Duration based on rhythm pattern
            duration = rhythm_pattern[i] if i < len(rhythm_pattern) else 0.5
            
            # Apply SAT solver duration modifications if available
            if sat_recommendations and 'duration_modifications' in sat_recommendations:
                if i < len(sat_recommendations['duration_modifications']):
                    duration *= sat_recommendations['duration_modifications'][i]
            
            # Add note with velocity based on emotional intensity and cultural influence
            velocity = int(60 + (score * 40) + (cultural_influence * 20))
            
            # Apply SAT solver velocity enhancements if available
            if sat_recommendations and 'velocity_enhancements' in sat_recommendations:
                if i < len(sat_recommendations['velocity_enhancements']):
                    velocity += sat_recommendations['velocity_enhancements'][i]
            
            midi.addNote(track_num, 0, pitch, time, duration, velocity)
            
            time += duration
    
    def _generate_harmony(self, midi, track_num, harmonic_progression, sentiment, scale, start_time):
        """Generate harmonic accompaniment with cultural scales."""
        if not harmonic_progression:
            return
            
        progression_type = 'happy' if sentiment > 0.5 else 'sad'
        chords = self.chord_progressions[progression_type]
        
        time = start_time
        chord_duration = 2.0  # Chords change every 2 beats
        
        for i, harmonic_value in enumerate(harmonic_progression):
            chord_index = i % len(chords)
            chord = chords[chord_index]
            base_note = 48 if sentiment > 0.5 else 45
            
            # Add chord notes using cultural scale
            for note_offset in chord:
                # Adjust note to fit cultural scale
                scale_note = scale[note_offset % len(scale)]
                pitch = base_note + scale_note
                midi.addNote(track_num, 1, pitch, time, chord_duration, 50)
            
            time += chord_duration
    
    def _generate_bass(self, midi, track_num, emotional_vector, sentiment, scale, start_time):
        """Generate bass line with cultural scale."""
        time = start_time
        base_note = 36 if sentiment > 0.5 else 33  # Root notes
        
        for i, score in enumerate(emotional_vector):
            if i % 2 == 0:  # Bass on every other note
                # Use scale notes for bass
                scale_note = scale[i % len(scale)]
                pitch = base_note + scale_note
                duration = 1.0
                midi.addNote(track_num, 2, pitch, time, duration, 80)
            time += 0.5
    
    def _generate_drums(self, midi, track_num, rhythm_pattern, arousal, cultural_context, start_time):
        """Generate drum pattern with cultural influences."""
        time = start_time
        pattern_length = len(rhythm_pattern) if rhythm_pattern else 8
        
        for i in range(pattern_length * 2):  # Double length for drums
            # Cultural drum patterns
            if cultural_context == 'african':
                # Complex polyrhythms
                if i % 3 == 0:
                    midi.addNote(track_num, 9, 36, time, 0.25, 100)  # Kick
                if i % 2 == 0:
                    midi.addNote(track_num, 9, 40, time, 0.125, 80)  # Tom
            elif cultural_context == 'latin':
                # Clave pattern influence
                if i % 4 in [0, 3]:
                    midi.addNote(track_num, 9, 36, time, 0.25, 100)  # Kick
                if i % 4 == 2:
                    midi.addNote(track_num, 9, 38, time, 0.25, 90)  # Snare
                if i % 2 == 1:
                    midi.addNote(track_num, 9, 42, time, 0.125, 70)  # Hi-hat
            else:  # western/eastern default
                # Standard rock pattern
                if i % 4 == 0:
                    midi.addNote(track_num, 9, 36, time, 0.25, 100)  # Kick
                if i % 4 == 2:
                    midi.addNote(track_num, 9, 38, time, 0.25, 90)  # Snare
            
            # Hi-hat on off-beats if high arousal
            if arousal > 0.6 and i % 2 == 1:
                midi.addNote(track_num, 9, 42, time, 0.125, 60)  # Hi-hat
            
            time += 0.5
    
    def _generate_pad(self, midi, track_num, sentiment, scale, start_time):
        """Generate atmospheric pad with cultural scale."""
        time = start_time
        base_note = 48 if sentiment > 0.5 else 45
        
        # Long sustained notes using cultural scale
        for i in range(4):
            scale_note = scale[i % len(scale)]
            pitch = base_note + scale_note
            midi.addNote(track_num, 3, pitch, time, 8.0, 40)
        time += 8.0

# Maintain backward compatibility
def generate_midi(emotional_vector, output_path="output.mid"):
    """Legacy function for backward compatibility."""
    generator = AdvancedMusicGenerator()
    
    # Convert old format to new format
    analysis_result = {
        'emotional_vector': emotional_vector,
        'sentiment': 0.5,
        'arousal': np.mean(emotional_vector) if emotional_vector else 0.5,
        'rhythm_pattern': [0.5 + (s * 0.5) for s in emotional_vector],
        'harmonic_progression': []
    }
    
    return generator.generate_midi(analysis_result, output_path)
