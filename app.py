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
import tensorflow as tf
from tensorflow import keras
from datetime import datetime
import base64
import io

# Configure TensorFlow to use minimal memory for Render free tier
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
# Disable GPU if available to save memory on free tier
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(f"GPU configuration error: {e}")
except Exception as e:
    print(f"GPU check failed: {e}")

# Limit TensorFlow to use only necessary memory and threads
try:
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(1)
except Exception as e:
    print(f"Threading config error: {e}")

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

# Load the trained model with memory optimization
print("Loading emotion recognition model...")
model = None
try:
    model_path = 'face_emotionModel.h5'
    if os.path.exists(model_path):
        # Load model with custom object scope to minimize memory
        # Don't compile on load - we only need inference, not training
        with tf.device('/CPU:0'):  # Use CPU to avoid GPU memory issues on free tier
            model = keras.models.load_model(model_path, compile=False)
        print("Model loaded successfully!")
    else:
        print(f"Warning: Model file '{model_path}' not found. Emotion detection will not work.")
        print("Please ensure face_emotionModel.h5 is in the project root directory.")
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    print(traceback.format_exc())
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
    Optimized for Render free tier with minimal memory usage.
    """
    if model is None:
        return None, "Model not loaded. Please train the model first."
    
    try:
        # Load and preprocess image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            return None, "Could not load image. Please ensure the file is a valid image."
        
        # Resize to 48x48 (model input size)
        img = cv2.resize(img, (48, 48))
        
        # Normalize pixel values to [0, 1]
        img = img.astype('float32') / 255.0
        
        # Reshape for model input: (1, 48, 48, 1)
        img = img.reshape(1, 48, 48, 1)
        
        # Predict emotion with CPU device and minimal memory
        # Use predict_on_batch for better memory efficiency
        try:
            with tf.device('/CPU:0'):  # Force CPU usage to avoid GPU memory issues
                # Use predict_on_batch for single prediction - more memory efficient
                predictions = model.predict_on_batch(img)
                emotion_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][emotion_idx])
                emotion = EMOTION_LABELS[emotion_idx]
            
            return emotion, confidence
        except Exception as pred_error:
            print(f"Prediction error: {pred_error}")
            import traceback
            print(traceback.format_exc())
            # Try alternative prediction method
            try:
                with tf.device('/CPU:0'):
                    predictions = model(img, training=False).numpy()
                    emotion_idx = np.argmax(predictions[0])
                    confidence = float(predictions[0][emotion_idx])
                    emotion = EMOTION_LABELS[emotion_idx]
                return emotion, confidence
            except Exception as alt_error:
                return None, f"Error during prediction: {str(pred_error)}"
        
    except Exception as e:
        import traceback
        print(f"Error in detect_emotion: {str(e)}")
        print(traceback.format_exc())
        return None, str(e)

def save_to_database(name, emotion, image_path):
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
        INSERT INTO users (name, emotion_detected, image_path, image_blob)
        VALUES (?, ?, ?, ?)
    ''', (name, emotion, image_path, image_blob))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint to keep service alive"""
    return {'status': 'healthy', 'model_loaded': model is not None}, 200

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    try:
        print("Form submission received")  # Debug log
        
        # Get form data
        name = request.form.get('name', '').strip()
        
        print(f"Form data - Name: {name}")  # Debug log
        
        # Validate required fields
        if not name:
            flash('Please enter your name.', 'error')
            return redirect(url_for('index'))
        
        # Check if image file is present
        if 'image' not in request.files:
            print("No image file in request")  # Debug log
            flash('Please upload an image.', 'error')
            return redirect(url_for('index'))
        
        file = request.files['image']
        
        if file.filename == '':
            print("Empty filename")  # Debug log
            flash('Please select an image file.', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            print(f"Invalid file type: {file.filename}")  # Debug log
            flash('Invalid file type. Please upload a valid image (PNG, JPG, JPEG, GIF, BMP).', 'error')
            return redirect(url_for('index'))
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            print(f"Created uploads directory: {app.config['UPLOAD_FOLDER']}")
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")  # Debug log
        
        # Detect emotion
        print("Starting emotion detection...")  # Debug log
        emotion, confidence = detect_emotion(filepath)
        
        if emotion is None:
            print(f"Emotion detection failed: {confidence}")  # Debug log
            flash(f'Error detecting emotion: {confidence}', 'error')
            # Clean up uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
            return redirect(url_for('index'))
        
        print(f"Emotion detected: {emotion} with confidence: {confidence}")  # Debug log
        
        # Save to database
        try:
            save_to_database(name, emotion, filepath)
            print("Data saved to database")  # Debug log
        except Exception as db_error:
            print(f"Database error: {db_error}")  # Debug log
            # Continue even if database save fails
        
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
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in submit: {str(e)}")  # Debug log
        print(f"Traceback: {error_trace}")  # Debug log
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

# Initialize database and uploads directory on app startup
# This runs when the module is imported (works with gunicorn)
init_database()
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print(f"Created uploads directory: {app.config['UPLOAD_FOLDER']}")

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Facial Emotion Recognition Web App")
    print("=" * 60)
    print("Server starting...")
    print("Access the app at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

