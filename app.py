from flask import Flask, request, send_file
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return {'error': 'No audio file provided'}, 400
    
    audio_file = request.files['audio']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'recording_{timestamp}.wav'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    audio_file.save(filepath)
    return {'message': 'Audio saved successfully', 'filename': filename}, 200

@app.route('/recordings/<filename>')
def get_recording(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return {'error': 'File not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)
