"""
Flask Web Application for Facial Emotion Recognition
This app allows users to submit their information and upload a picture.
It detects emotions and stores data in SQLite database.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sqlite3
import numpy as np
from PIL import Image
import cv2
from tensorflow import keras
from datetime import datetime
import base64
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Emotion labels mapping
EMOTION_LABELS = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral'
}

# Emotion messages mapping
EMOTION_MESSAGES = {
    'Angry': "You look angry. What's making you upset?",
    'Disgust': "You seem disgusted. What's bothering you?",
    'Fear': "You appear fearful. What are you afraid of?",
    'Happy': "You're smiling! What's making you happy?",
    'Sad': "You are frowning. Why are you sad?",
    'Surprise': "You look surprised! What caught you off guard?",
    'Neutral': "You have a neutral expression. How are you feeling?"
}

# Load the trained model
print("Loading emotion recognition model...")
try:
    model = keras.models.load_model('face_emotionModel.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please train the model first using model_training.py")
    model = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create table for storing user data and images
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            student_id TEXT,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            emotion_detected TEXT,
            image_path TEXT,
            image_blob BLOB
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def detect_emotion(image_path):
    """
    Detect emotion from an image file.
    Preprocesses the image and uses the trained model for prediction.
    """
    if model is None:
        return None, "Model not loaded. Please train the model first."
    
    try:
        # Load and preprocess image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Resize to 48x48 (model input size)
        img = cv2.resize(img, (48, 48))
        
        # Normalize pixel values to [0, 1]
        img = img.astype('float32') / 255.0
        
        # Reshape for model input: (1, 48, 48, 1)
        img = img.reshape(1, 48, 48, 1)
        
        # Predict emotion
        predictions = model.predict(img, verbose=0)
        emotion_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][emotion_idx])
        emotion = EMOTION_LABELS[emotion_idx]
        
        return emotion, confidence
        
    except Exception as e:
        return None, str(e)

def save_to_database(name, email, student_id, emotion, image_path):
    """Save user data and image to database"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Read image as binary
    image_blob = None
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_blob = f.read()
    
    # Insert into database
    cursor.execute('''
        INSERT INTO users (name, email, student_id, emotion_detected, image_path, image_blob)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, student_id, emotion, image_path, image_blob))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        student_id = request.form.get('student_id', '').strip()
        
        # Validate required fields
        if not name or not email:
            flash('Please fill in all required fields (Name and Email).', 'error')
            return redirect(url_for('index'))
        
        # Check if image file is present
        if 'image' not in request.files:
            flash('Please upload an image.', 'error')
            return redirect(url_for('index'))
        
        file = request.files['image']
        
        if file.filename == '':
            flash('Please select an image file.', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a valid image (PNG, JPG, JPEG, GIF, BMP).', 'error')
            return redirect(url_for('index'))
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Detect emotion
        emotion, confidence = detect_emotion(filepath)
        
        if emotion is None:
            flash(f'Error detecting emotion: {confidence}', 'error')
            return redirect(url_for('index'))
        
        # Save to database
        save_to_database(name, email, student_id, emotion, filepath)
        
        # Get emotion message
        message = EMOTION_MESSAGES.get(emotion, f"You look {emotion.lower()}.")
        
        # Display result
        flash(f'Success! Emotion detected: {emotion} (Confidence: {confidence:.2%})', 'success')
        flash(f'{message}', 'info')
        
        return render_template('index.html', 
                             emotion=emotion, 
                             message=message, 
                             confidence=f"{confidence:.2%}",
                             name=name)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    print("\n" + "=" * 60)
    print("Facial Emotion Recognition Web App")
    print("=" * 60)
    print("Server starting...")
    print("Access the app at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

