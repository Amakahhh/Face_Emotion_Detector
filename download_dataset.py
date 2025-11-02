"""
Helper script to download FER2013 dataset from Kaggle.
This script requires Kaggle API credentials to be set up.
"""

import os
import subprocess
import sys

def check_kaggle_installed():
    """Check if kaggle package is installed"""
    try:
        import kaggle
        return True
    except ImportError:
        return False

def download_with_kaggle_api():
    """Download dataset using Kaggle API"""
    print("=" * 60)
    print("Downloading FER2013 dataset using Kaggle API")
    print("=" * 60)
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        print("Kaggle API authenticated successfully!")
        print("Downloading dataset...")
        
        # Download the dataset
        api.dataset_download_files(
            'msambare/fer2013',
            path='.',
            unzip=True
        )
        
        # Look for fer2013.csv
        if os.path.exists('fer2013.csv'):
            print("\n[SUCCESS] fer2013.csv downloaded successfully!")
            print(f"File size: {os.path.getsize('fer2013.csv') / (1024*1024):.2f} MB")
            return True
        else:
            print("\n[WARNING] Dataset downloaded but fer2013.csv not found.")
            print("Please check the downloaded files.")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Error downloading dataset: {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("FER2013 Dataset Download Helper")
    print("=" * 60 + "\n")
    
    # Check if file already exists
    if os.path.exists('fer2013.csv'):
        print("[OK] fer2013.csv already exists in the current directory!")
        print("No need to download again.")
        return
    
    print("FER2013 dataset is required for training the emotion recognition model.")
    print("\nDownload Options:")
    print("1. Using Kaggle API (automated)")
    print("2. Manual download (recommended for first-time users)")
    print("\n" + "-" * 60)
    
    # Check if kaggle is installed
    if check_kaggle_installed():
        print("\n[OK] Kaggle package is installed!")
        print("Attempting to download using Kaggle API...")
        
        if download_with_kaggle_api():
            return
        else:
            print("\n[WARNING] Kaggle API download failed. Please use manual method.")
    else:
        print("\n[INFO] Kaggle package not installed.")
        print("Installing kaggle package...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            print("[OK] Kaggle package installed!")
            
            if download_with_kaggle_api():
                return
        except Exception as e:
            print(f"[WARNING] Could not install kaggle package: {e}")
    
    # Manual instructions
    print("\n" + "=" * 60)
    print("MANUAL DOWNLOAD INSTRUCTIONS")
    print("=" * 60)
    print("\n1. Go to: https://www.kaggle.com/datasets/msambare/fer2013")
    print("2. Sign up for a free Kaggle account (if needed)")
    print("3. Click 'Download' button")
    print("4. Extract the ZIP file")
    print("5. Copy 'fer2013.csv' to this directory:")
    print(f"   {os.getcwd()}")
    print("\n[IMPORTANT] You may need to accept the dataset terms on Kaggle first!")
    print("\nAfter downloading, run this script again or proceed to training.")

if __name__ == '__main__':
    main()
