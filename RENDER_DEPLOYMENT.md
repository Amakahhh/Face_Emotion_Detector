# 🌐 Render Deployment Guide

Deploy your Facial Emotion Recognition app to Render (Free Tier Available!)

## Prerequisites

✅ GitHub repository created and code pushed
✅ Model trained (`face_emotionModel.h5` exists)
✅ All files ready in GitHub repo

## Step 1: Create Render Account

1. Go to [Render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with:
   - Email + Password OR
   - GitHub account (recommended - easier to connect)

## Step 2: Create New Web Service

1. After logging in, click **"New +"** button (top right)
2. Select **"Web Service"**

## Step 3: Connect GitHub Repository

1. Click **"Connect GitHub"** or **"Connect GitLab"** (if you used GitLab)
2. Authorize Render to access your repositories
3. Select your repository: `facial-emotion-recognition` (or your repo name)

## Step 4: Configure Your Service

Fill in the following settings:

### Basic Settings

- **Name:** `emotion-recognition-app` (or your preferred name)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main` (or `master` if you used that)

### Build & Deploy

- **Runtime:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  gunicorn app:app
  ```

### Advanced Settings (Optional)

- **Instance Type:** Free (or upgrade to paid for better performance)
- **Auto-Deploy:** Yes (automatically deploy on every push)

## Step 5: Add Environment Variables (If Needed)

Usually not required for this app, but if you need:
1. Go to "Environment" tab
2. Add any variables (e.g., `SECRET_KEY`, etc.)

## Step 6: Deploy

1. Click **"Create Web Service"** button
2. Render will start building and deploying your app
3. Wait 5-10 minutes for deployment

## Step 7: Get Your Live URL

1. Once deployment completes (green status), you'll see:
   - **URL:** `https://your-app-name.onrender.com`
2. Copy this URL
3. Save it to `link_web_app.txt`:
   ```bash
   https://your-app-name.onrender.com
   ```

## Step 8: Verify Deployment

1. Open your Render URL in a browser
2. Test uploading an image
3. Verify emotion detection works

## ⚠️ Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- **May take 30-60 seconds to wake up**
- **Limited to 750 hours/month** (usually plenty)
- **512MB RAM**

### Model File Size

- Make sure `face_emotionModel.h5` is in your GitHub repo
- If file is too large (>100MB), consider:
  - Using Git LFS (Large File Storage)
  - Or hosting model separately

### Database on Render

- The `database.db` file will be created automatically
- **Note:** Free tier has ephemeral filesystem (data may be lost on restart)
- For production, consider using Render PostgreSQL (paid tier)

### Adding Persistent Disk (Optional)

For production use:
1. Go to Render Dashboard
2. Create a "Persistent Disk"
3. Mount it to store database and uploads

## 🔄 Updating Your App

Every time you push to GitHub:
1. Render automatically detects changes
2. Rebuilds and redeploys your app
3. Updates go live automatically!

## 📊 Monitoring

- Check "Logs" tab for any errors
- Check "Metrics" for performance
- Check "Events" for deployment history

## 🐛 Troubleshooting

### "Build failed"
- Check build logs in Render dashboard
- Make sure `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`

### "Application error"
- Check application logs
- Make sure `face_emotionModel.h5` exists in repo
- Verify all paths are correct

### "Module not found"
- Check `requirements.txt` includes all packages
- Verify build completed successfully

### "Model file not found"
- Make sure `face_emotionModel.h5` is committed to GitHub
- Check file exists in root directory

## 📝 Next Steps After Deployment

1. ✅ Save deployment URL to `link_web_app.txt`
2. ✅ Test the live application
3. ✅ Share the link with users!

---

**Need help?** Check Render documentation: https://render.com/docs

