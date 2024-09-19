from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import zipfile
import json
import pandas as pd

app = Flask(__name__)

# Set the path for uploaded files
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Optionally, you can immediately process the file here
    # data = process_zip(file_path)

    return jsonify({'success': 'File uploaded successfully', 'filename': file.filename})

# Route to analyze the uploaded file
@app.route('/analyze', methods=['POST'])
def analyze_data():
    # Check if there is any file in the uploads folder
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return jsonify({'error': 'No files found in the uploads folder'}), 400
    
    # Assume there is only one file in the folder for simplicity
    zip_path = os.path.join(UPLOAD_FOLDER, files[0])

    # Process the uploaded file and extract data
    data = process_zip(zip_path)

    return jsonify(data)

def process_zip(zip_path):
    extracted_data = {}

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)
        
        # For example, parse watch history
        watch_history_file = os.path.join(UPLOAD_FOLDER, 'YouTube and YouTube Music/history/watch-history.json')
        if os.path.exists(watch_history_file):
            with open(watch_history_file, 'r') as f:
                watch_history = json.load(f)
                extracted_data['watch_history'] = parse_watch_history(watch_history)
        
    return extracted_data

def parse_watch_history(watch_history):
    watch_time_per_day = {}

    for entry in watch_history:
        date = entry.get('time').split('T')[0]
        watch_time_per_day[date] = watch_time_per_day.get(date, 0) + 1  # Assuming each entry represents a single video watched
    
    # Convert to DataFrame and return for frontend visualization
    df = pd.DataFrame(list(watch_time_per_day.items()), columns=['Date', 'Videos_Watched'])
    return df.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
