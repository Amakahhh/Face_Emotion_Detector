# 🚀 GitHub Repository Setup Guide

## Step 1: Initialize Git Repository

Open PowerShell/Terminal in your project directory and run:

```bash
cd "c:\Users\DELL 7300\pace website\Ejike_22CG031853"
git init
```

## Step 2: Create .gitignore (Already Created!)

The `.gitignore` file is already created to exclude:
- Database files
- Model files (you'll add these after training)
- Upload folders
- Python cache files

## Step 3: Stage All Files

```bash
git add .
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Facial Emotion Recognition Web App"
```

## Step 5: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it: `facial-emotion-recognition` (or your preferred name)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 6: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name

## Step 7: Push Your Code

```bash
git push -u origin main
```

You may be asked to authenticate. Use:
- Personal Access Token (recommended) OR
- GitHub CLI

## ✅ What Gets Uploaded

**Files that WILL be uploaded:**
- ✅ app.py
- ✅ model_training.py
- ✅ requirements.txt
- ✅ templates/index.html
- ✅ README.md
- ✅ All helper scripts
- ✅ .gitignore

**Files that WON'T be uploaded (via .gitignore):**
- ❌ database.db (created automatically)
- ❌ face_emotionModel.h5 (add this after training)
- ❌ fer2013.csv (too large, download separately)
- ❌ uploads/ folder

## 📝 Note About Model File

**Important:** After training the model, you'll need to add `face_emotionModel.h5` to GitHub for Render deployment:

1. Train the model first: `python model_training.py`
2. After training completes, add the model file:
   ```bash
   git add face_emotionModel.h5
   git commit -m "Add trained emotion recognition model"
   git push
   ```

## 🔗 Next Steps

After pushing to GitHub:
1. Go to Render deployment guide: `RENDER_DEPLOYMENT.md`
2. Connect your GitHub repo to Render
3. Deploy your application!

---

**Troubleshooting:**

### "Permission denied" error
- Make sure you're authenticated with GitHub
- Use Personal Access Token instead of password

### "Large file" error
- Make sure fer2013.csv is in .gitignore
- Don't commit large files (>100MB)

### Need to update .gitignore
- Edit `.gitignore` file
- Add files you want to exclude

