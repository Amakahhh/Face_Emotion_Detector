# 📥 FER2013 Dataset Download Guide

## Quick Start Options

### Option 1: Automated Download (Requires Kaggle API Setup)

1. **Install Kaggle package:**
   ```bash
   pip install kaggle
   ```

2. **Set up Kaggle API credentials:**
   - Go to https://www.kaggle.com/account
   - Scroll down to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json` file
   - **Windows:** Copy `kaggle.json` to `C:\Users\<YourUsername>\.kaggle\`
   - **Mac/Linux:** Copy `kaggle.json` to `~/.kaggle/`
   - **Important:** Make sure the file has proper permissions (readable by owner only)

3. **Run the download script:**
   ```bash
   python download_dataset.py
   ```

### Option 2: Manual Download (Recommended for Beginners)

1. **Visit the Kaggle Dataset:**
   - Go to: https://www.kaggle.com/datasets/msambare/fer2013

2. **Sign Up/Login:**
   - Create a free Kaggle account if you don't have one
   - Login to your account

3. **Accept Terms:**
   - On the dataset page, you may see a notice to accept the dataset terms
   - Click "I Understand and Accept" if prompted

4. **Download:**
   - Click the "Download" button (usually top right)
   - Wait for the download to complete

5. **Extract and Place:**
   - Extract the ZIP file
   - Find `fer2013.csv` inside
   - Copy `fer2013.csv` to your project root directory:
     ```
     C:\Users\DELL 7300\pace website\Ejike_22CG031853\fer2013.csv
     ```

6. **Verify:**
   - Check that `fer2013.csv` is in the same folder as `app.py` and `model_training.py`
   - File should be approximately 120-150 MB in size

## Alternative: Direct Link (If Available)

If you're logged into Kaggle, you can try this direct download link:
- https://www.kaggle.com/datasets/msambare/fer2013/download

## File Verification

After downloading, verify the file:
- **Filename:** `fer2013.csv`
- **Location:** Same directory as `app.py`
- **Size:** Approximately 120-150 MB
- **Format:** CSV file with columns: emotion, pixels, Usage

## Next Steps

Once `fer2013.csv` is in place:

1. **Train the model:**
   ```bash
   python model_training.py
   ```

2. **Wait for training to complete** (1-2 hours)

3. **Run the web app:**
   ```bash
   python app.py
   ```

## Troubleshooting

### "File not found" error
- Make sure `fer2013.csv` is in the project root directory
- Check the filename is exactly `fer2013.csv` (case-sensitive)

### Kaggle API errors
- Make sure `kaggle.json` is in the correct location
- Check file permissions on `kaggle.json`
- Try manual download instead

### Download failed
- Make sure you're logged into Kaggle
- Accept the dataset terms if prompted
- Check your internet connection

---

**Need help?** Check the main README.md file for more information.
