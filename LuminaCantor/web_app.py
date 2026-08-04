from flask import Flask, render_template, request, send_file, jsonify
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LuminaCantor.cognitive_matrix_composer import CognitiveMatrixComposer
from LuminaCantor.music_production_integration import MusicProductionIntegrator

try:
    from LuminaCantor.pulse_mapper import PulseMapper, BioFeedbackLoop
    PULSE_MAPPER_AVAILABLE = True
except ImportError:
    PULSE_MAPPER_AVAILABLE = False

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Cognitive Matrix Composer (industrial-grade system)
cognitive_composer = CognitiveMatrixComposer()
production_integrator = MusicProductionIntegrator()

# Initialize bio-feedback system if available
if PULSE_MAPPER_AVAILABLE:
    pulse_mapper = PulseMapper()
    bio_feedback_loop = BioFeedbackLoop()
    print("  [WEB APP]: Bio-feedback system initialized")
else:
    pulse_mapper = None
    bio_feedback_loop = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transmute', methods=['POST'])
def transmute():
    text = request.form.get('text')
    user_id = request.form.get('user_id', 'anonymous')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Use Cognitive Matrix Composer for industrial-grade generation
        result = cognitive_composer.compose_music(text, user_id)
        
        if not result['success']:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
        
        analysis_result = result['analysis']
        
        # Handle missing emotional_vector gracefully
        emotional_vector = analysis_result.get('emotional_vector', [])
        
        return jsonify({
            'success': True,
            'message': f'Transmuted {len(emotional_vector)} emotional points into orchestral music',
            'data_points': len(emotional_vector),
            'sentiment': analysis_result.get('sentiment', 0.5),
            'arousal': analysis_result.get('arousal', 0.5),
            'complexity': analysis_result.get('complexity', 0.5),
            'cultural_context': analysis_result.get('cultural_context', 'western'),
            'cultural_influence': analysis_result.get('cultural_influence', 0.0),
            'generation_time': result.get('generation_time', 0.0),
            'cache_hit': result.get('cache_hit', False),
            'sat_cache_hit': result.get('sat_cache_hit', False),
            'session_id': result.get('session_id', ''),
            'analysis': {
                'sentiment': f"{analysis_result.get('sentiment', 0.5):.2f}",
                'arousal': f"{analysis_result.get('arousal', 0.5):.2f}",
                'complexity': f"{analysis_result.get('complexity', 0.5):.2f}",
                'valence': f"{analysis_result.get('valence', 0.5):.2f}",
                'cultural_context': analysis_result.get('cultural_context', 'western'),
                'cultural_influence': f"{analysis_result.get('cultural_influence', 0.0):.2f}"
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download():
    output_path = os.path.join(os.path.dirname(__file__), 'temp_output.mid')
    if not os.path.exists(output_path):
        return jsonify({'error': 'No MIDI file generated yet'}), 404
    return send_file(output_path, as_attachment=True, download_name='transmutation.mid')

@app.route('/translate-culture', methods=['POST'])
def translate_culture():
    """Translate emotional content to a different cultural context."""
    text = request.form.get('text')
    target_culture = request.form.get('target_culture', 'western')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Analyze original text
        analysis_result = cognitive_composer.parser.parse(text)
        
        # Translate to target culture
        translated_profile = cognitive_composer.empathy_engine.translate_emotional_content(
            analysis_result['cultural_profile'], target_culture
        )
        
        # Generate music with translated parameters
        translated_analysis = analysis_result.copy()
        translated_analysis['sentiment'] = translated_profile['translated_sentiment']
        translated_analysis['arousal'] = translated_profile['translated_arousal']
        translated_analysis['cultural_context'] = target_culture
        
        output_path = os.path.join(os.path.dirname(__file__), f'temp_output_{target_culture}.mid')
        cognitive_composer.generator.generate_midi(translated_analysis, output_path)
        
        return jsonify({
            'success': True,
            'translation': translated_profile,
            'message': f'Translated from {translated_profile["source_culture"]} to {target_culture}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for learning."""
    data = request.json
    
    try:
        # Get the analysis result that generated this music
        # In production, would store this with the session
        analysis_result = {
            'cultural_context': data.get('cultural_context', 'western'),
            'sentiment': data.get('sentiment', 0.5),
            'arousal': data.get('arousal', 0.5),
            'complexity': data.get('complexity', 0.5),
            'sat_recommendations': data.get('sat_used', False)
        }
        
        feedback_data = {
            'input_text': data.get('input_text', ''),
            'rating': data.get('rating', 0),
            'liked_aspects': data.get('liked_aspects', []),
            'disliked_aspects': data.get('disliked_aspects', []),
            'comments': data.get('comments', '')
        }
        
        user_id = data.get('user_id', 'anonymous')
        feedback_record = cognitive_composer.learning_engine.record_feedback(user_id, analysis_result, feedback_data)
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded successfully',
            'feedback_id': len(cognitive_composer.learning_engine.feedback_history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_project():
    """Export to professional music production formats."""
    format_type = request.form.get('format', 'all')
    project_name = request.form.get('project_name', 'alchemical_cantor')
    
    try:
        midi_path = os.path.join(os.path.dirname(__file__), 'temp_output.mid')
        
        # Get the last analysis result (in production, would store in session)
        analysis_result = {
            'sentiment': 0.5,
            'arousal': 0.5,
            'cultural_context': 'western',
            'complexity': 0.5
        }
        
        if format_type == 'all':
            exports = production_integrator.export_all_formats(midi_path, analysis_result, project_name)
        elif format_type == 'ableton':
            exports = {'ableton': production_integrator.export_to_ableton(midi_path, project_name)}
        elif format_type == 'fl_studio':
            exports = {'fl_studio': production_integrator.export_to_fl_studio(midi_path, project_name)}
        elif format_type == 'musicxml':
            exports = {'musicxml': production_integrator.export_to_musicxml(midi_path, analysis_result)}
        else:
            return jsonify({'error': 'Unsupported format'}), 400
        
        return jsonify({
            'success': True,
            'exports': exports,
            'message': f'Exported to {len(exports)} format(s)'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics')
def get_metrics():
    """Get system learning and performance metrics."""
    try:
        learning_metrics = cognitive_composer.learning_engine.get_learning_metrics()
        empathy_metrics = cognitive_composer.empathy_engine.generate_empathy_metrics()
        supported_formats = production_integrator.get_supported_formats()
        
        return jsonify({
            'success': True,
            'learning_metrics': learning_metrics,
            'empathy_metrics': empathy_metrics,
            'supported_formats': supported_formats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bio-feedback/start', methods=['POST'])
def start_bio_feedback():
    """Start bio-feedback loop for therapeutic music generation."""
    if not PULSE_MAPPER_AVAILABLE:
        return jsonify({'error': 'Bio-feedback system not available'}), 503
    
    try:
        initial_bpm = request.json.get('initial_bpm', 70.0)
        success = bio_feedback_loop.start_feedback_loop(initial_bpm)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Bio-feedback loop started successfully'
            })
        else:
            return jsonify({'error': 'Failed to start bio-feedback loop'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bio-feedback/process', methods=['POST'])
def process_biometric_sample():
    """Process biometric sample and generate music adjustments."""
    if not PULSE_MAPPER_AVAILABLE:
        return jsonify({'error': 'Bio-feedback system not available'}), 503
    
    try:
        bpm = request.json.get('bpm', 70.0)
        cultural_context = request.json.get('cultural_context', 'western')
        
        result = bio_feedback_loop.process_biometric_sample(bpm)
        
        return jsonify({
            'success': True,
            'biometric_data': result['biometric_data'],
            'recommendations': result['recommendations'],
            'packet_size': result['packet_size'],
            'intervention_needed': result['recommendations'].get('intervention_needed', False)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bio-feedback/stop', methods=['POST'])
def stop_bio_feedback():
    """Stop bio-feedback loop."""
    if not PULSE_MAPPER_AVAILABLE:
        return jsonify({'error': 'Bio-feedback system not available'}), 503
    
    try:
        success = bio_feedback_loop.stop_feedback_loop()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Bio-feedback loop stopped successfully'
            })
        else:
            return jsonify({'error': 'Failed to stop bio-feedback loop'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bio-feedback/history', methods=['GET'])
def get_intervention_history():
    """Get history of therapeutic interventions."""
    if not PULSE_MAPPER_AVAILABLE:
        return jsonify({'error': 'Bio-feedback system not available'}), 503
    
    try:
        history = bio_feedback_loop.get_intervention_history()
        
        return jsonify({
            'success': True,
            'intervention_history': history,
            'total_interventions': len(history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bio-feedback/simulate', methods=['POST'])
def simulate_biometric_stream():
    """Simulate bio-signal stream for testing."""
    if not PULSE_MAPPER_AVAILABLE:
        return jsonify({'error': 'Bio-feedback system not available'}), 503
    
    try:
        duration = request.json.get('duration', 10.0)
        data_stream = pulse_mapper.simulate_project_aegis_stream(duration)
        
        return jsonify({
            'success': True,
            'data_points': len(data_stream),
            'duration': duration,
            'sample_data': data_stream[:5]  # Return first 5 samples
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
