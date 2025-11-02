# Facial Emotion Recognition Web Application

A machine learning web application that detects emotions from facial images using a CNN model trained on the FER2013 dataset.

## 📋 Project Overview

This project allows users to:
- Upload their photo through a web interface
- Get real-time emotion detection (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)
- Have their information and image stored in a SQLite database

## 🏗️ Project Structure

```
/
├── app.py                  # Flask web application
├── model_training.py       # CNN model training script
├── requirements.txt       # Python dependencies
├── database.db            # SQLite database (created automatically)
├── face_emotionModel.h5   # Trained model (created after training)
├── link_web_app.txt       # Render deployment link (add after deployment)
├── templates/
│   └── index.html         # Front-end interface
└── uploads/               # Uploaded images (created automatically)
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download FER2013 Dataset

The FER2013 dataset is required to train the model. Here's how to get it:

1. **Option A: Download from Kaggle** (Recommended)
   - Go to [Kaggle FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)
   - You'll need a Kaggle account (free)
   - Download the `fer2013.csv` file
   - Place it in the project root directory

2. **Option B: Use Direct Download**
   - Visit the original FER2013 challenge page
   - Or search for "FER2013 dataset download" online
   - Download the CSV file and place it in the project root

**Important:** The file should be named `fer2013.csv` and placed in the same directory as `model_training.py`

### Step 3: Train the Model

Once you have the `fer2013.csv` file, train the model:

```bash
python model_training.py
```

**Note:** Training may take 1-2 hours depending on your computer's performance. The script will:
- Load and preprocess the FER2013 dataset
- Create a CNN model architecture
- Train the model for up to 50 epochs
- Save the best model as `face_emotionModel.h5`

### Step 4: Run the Web Application

After training is complete, start the Flask server:

```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

Open this URL in your web browser and start uploading images!

## 📝 How It Works

### Model Training (`model_training.py`)
1. **Data Loading**: Reads `fer2013.csv` which contains 48x48 grayscale images
2. **Preprocessing**: Converts pixel strings to numpy arrays, normalizes values
3. **Model Architecture**: Creates a CNN with:
   - 3 convolutional blocks (32, 64, 128 filters)
   - Batch normalization and dropout for regularization
   - Dense layers for final classification
4. **Training**: Trains on 28,709 images, validates on 3,589 images
5. **Saving**: Saves the best model as `face_emotionModel.h5`

### Web Application (`app.py`)
1. **Server**: Flask web server handles HTTP requests
2. **Image Upload**: Accepts image files (PNG, JPG, etc.)
3. **Preprocessing**: Converts uploaded image to 48x48 grayscale
4. **Prediction**: Uses the trained model to detect emotion
5. **Storage**: Saves user info and image to SQLite database
6. **Response**: Displays emotion result with a personalized message

### Database (`database.db`)
Stores:
- User name, email, student ID
- Detected emotion
- Image path and binary data
- Submission timestamp

## 🎯 Emotions Detected

The model detects 7 emotions:
- **Angry** (0)
- **Disgust** (1)
- **Fear** (2)
- **Happy** (3)
- **Sad** (4)
- **Surprise** (5)
- **Neutral** (6)

## 🌐 Deployment on Render

### Prerequisites
1. GitHub account
2. Render account (free tier available)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Facial Emotion Recognition App"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [Render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: emotion-recognition-app (or your choice)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free (or paid if preferred)
   - Click "Create Web Service"
   - Wait for deployment (usually 5-10 minutes)

3. **Important for Render**
   - Make sure `face_emotionModel.h5` is included in your GitHub repo (or upload it via Render's file system)
   - The database will be created automatically on Render
   - For production, consider using Render's persistent disk for the database

4. **Get Deployment Link**
   - Once deployed, copy the public URL from Render
   - Save it to `link_web_app.txt`

## 🐛 Troubleshooting

### Model not found error
- Make sure you've trained the model first using `model_training.py`
- Ensure `face_emotionModel.h5` exists in the project root

### Dataset not found error
- Download `fer2013.csv` from Kaggle
- Place it in the same directory as `model_training.py`

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- For TensorFlow issues, try: `pip install --upgrade tensorflow`

### Database errors
- The database will be created automatically when you run `app.py`
- If issues persist, delete `database.db` and restart the app

## 📚 Technologies Used

- **Python 3.x**: Programming language
- **Flask**: Web framework
- **TensorFlow/Keras**: Deep learning framework
- **OpenCV**: Image processing
- **SQLite**: Database
- **NumPy/Pandas**: Data processing
- **Pillow**: Image handling

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as part of a machine learning project for facial emotion recognition.

---

**Happy Coding! 🚀**
