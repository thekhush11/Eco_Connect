import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from typing import Optional, List, Any # Import for clean type hinting

# Fix the path to import from the utils folder correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
# PYLANCE FIX: Ignore the inability to statically resolve the import path
from recommend import classify_image, get_recommendation_logic # type: ignore 

# 1. Setup Flask App with CORRECT paths
app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../static') 
app.secret_key = 'eco_connect_secure_key_123' 

# 2. Configure Upload Folder (Points to Eco_Connect/static/uploads)
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# --- ROUTE HANDLERS ---

@app.route('/')
def home() -> str:
    return render_template('index.html')

@app.route('/upload')
def upload_page() -> str:
    return render_template('upload.html')

@app.route('/upload_action', methods=['POST'])
def upload_action() -> Any:
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename is None or file.filename == '':
        return redirect(url_for('upload_page'))
    
    # The filename is guaranteed to be a string now, satisfying Pylance
    filename: str = secure_filename(file.filename) 
    
    if filename:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Call AI Module
        label, confidence, components = classify_image(filepath)
        
        # Save results in Session
        session['uploaded_image'] = filename
        session['label'] = label
        session['confidence'] = confidence
        session['components'] = components
        
        return redirect(url_for('classify_page'))
    return redirect(url_for('upload_page'))

# Route to serve the classified image from the uploads folder
@app.route('/static/uploads/<filename>')
def uploaded_file(filename: str) -> Any:
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'uploads'), filename)

@app.route('/classify')
def classify_page() -> str:
    # Retrieve data from session, providing default types to satisfy Pylance
    image_file: Optional[str] = session.get('uploaded_image', 'default.jpg')
    label: Optional[str] = session.get('label', 'Unknown')
    confidence: Optional[str] = session.get('confidence', '0.00')
    components: Optional[List[str]] = session.get('components', [])

    return render_template('classify.html', 
                           label=label,
                           confidence=confidence,
                           components=components,
                           image_url=url_for('uploaded_file', filename=image_file or 'default.jpg')) # Added 'or default.jpg' safety check

@app.route('/questions')
def questions_page() -> str:
    return render_template('questions.html')

@app.route('/recommendations', methods=['POST'])
def recommendations_page() -> str:
    condition = request.form.get('condition', 'N/A')
    intent = request.form.get('intent', 'N/A')
    
    label = session.get('label', 'General Waste')
    
    rec_data = get_recommendation_logic(label, condition, intent)
    
    return render_template('recommendations.html', 
                           rec=rec_data,
                           centers=rec_data['centers'])

@app.route('/feedback')
def feedback_page() -> str:
    return render_template('feedback.html')

if __name__ == '__main__':
    print("Starting Eco Connect Server...")
    print("Go to http://127.0.0.1:5000 in your browser")
    app.run(debug=True, port=5000)