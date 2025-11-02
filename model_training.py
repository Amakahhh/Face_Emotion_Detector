"""
Facial Emotion Recognition Model Training Script
This script trains a CNN model on the FER2013 dataset to recognize emotions.
Emotions: 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os

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

def load_fer2013_data(csv_path='fer2013.csv'):
    """
    Load and preprocess FER2013 dataset from CSV file.
    
    The CSV should have columns: emotion, pixels, Usage
    - emotion: 0-6 (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)
    - pixels: space-separated pixel values (48x48 grayscale image)
    - Usage: 'Training', 'PublicTest', or 'PrivateTest'
    """
    print("Loading FER2013 dataset...")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"FER2013 CSV file not found at {csv_path}\n"
            "Please download fer2013.csv from Kaggle and place it in the project root."
        )
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Split by usage
    train_df = df[df['Usage'] == 'Training']
    val_df = df[df['Usage'] == 'PublicTest']
    test_df = df[df['Usage'] == 'PrivateTest']
    
    # Convert pixel strings to numpy arrays
    def pixels_to_array(pixel_str):
        return np.array([int(pixel) for pixel in pixel_str.split()], dtype=np.float32)
    
    # Process training data
    print("Processing training data...")
    X_train = np.array([pixels_to_array(pixels) for pixels in train_df['pixels']])
    y_train = train_df['emotion'].values
    
    # Process validation data
    print("Processing validation data...")
    X_val = np.array([pixels_to_array(pixels) for pixels in val_df['pixels']])
    y_val = val_df['emotion'].values
    
    # Process test data
    print("Processing test data...")
    X_test = np.array([pixels_to_array(pixels) for pixels in test_df['pixels']])
    y_test = test_df['emotion'].values
    
    # Reshape to (samples, 48, 48, 1) for CNN input
    X_train = X_train.reshape(-1, 48, 48, 1)
    X_val = X_val.reshape(-1, 48, 48, 1)
    X_test = X_test.reshape(-1, 48, 48, 1)
    
    # Normalize pixel values to [0, 1]
    X_train = X_train / 255.0
    X_val = X_val / 255.0
    X_test = X_test / 255.0
    
    # One-hot encode labels
    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

def create_model(input_shape=(48, 48, 1), num_classes=7):
    """
    Create a CNN model for emotion recognition.
    
    Architecture:
    - Conv2D layers with increasing filters
    - MaxPooling after each conv block
    - BatchNormalization for stability
    - Dropout to prevent overfitting
    - Dense layers for classification
    """
    model = Sequential([
        # First Conv Block
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape, padding='same'),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Second Conv Block
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Third Conv Block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Flatten and Dense Layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model():
    """
    Main training function.
    Loads data, creates model, trains, and saves the model.
    """
    print("=" * 60)
    print("FACIAL EMOTION RECOGNITION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_fer2013_data()
    
    # Create model
    print("\nCreating CNN model...")
    model = create_model()
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel Architecture:")
    model.summary()
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        'face_emotionModel.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    # Train model
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)
    
    history = model.fit(
        X_train, y_train,
        batch_size=64,
        epochs=50,
        validation_data=(X_val, y_val),
        callbacks=[checkpoint, early_stop],
        verbose=1
    )
    
    # Evaluate on test set
    print("\n" + "=" * 60)
    print("Evaluating on test set...")
    print("=" * 60)
    model.load_weights('face_emotionModel.h5')
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"\nTest Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    print("\n" + "=" * 60)
    print("Training completed! Model saved as 'face_emotionModel.h5'")
    print("=" * 60)

if __name__ == '__main__':
    train_model()

