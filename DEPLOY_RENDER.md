# Deploy Smart Attendance System to Render

## Prerequisites
- GitHub account with the repository connected
- Render account (free tier available at https://render.com)

## Deployment Steps

### Option 1: Quick Deploy via Render Dashboard

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up/Login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `antonyathibana/FINAL-YEAR-PROJECT`
   - Select the `main` branch

3. **Configure Service**
   - **Name**: `smart-attendance-system`
   - **Environment**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Add Environment Variables** (Optional - auto-generated)
   - `SECRET_KEY`: (Render will auto-generate a secure key)
   - `PYTHON_VERSION`: `3.11`

5. **Create Web Service**
   - Select "Free" plan
   - Click "Create Web Service"

### Option 2: Deploy via render.yaml (Auto-Deploy)

1. **Connect GitHub Repository**
   - Go to https://dashboard.render.com/blueprints
   - Click "New Blueprint Instance"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

2. **Verify Deployment**
   - Render will automatically deploy
   - Check build logs for errors
   - Visit your deployed URL

## After Deployment

### Important Notes for Face Recognition on Render

⚠️ **Render Free Tier Limitations:**
- Web services on free tier go to sleep after 15 minutes of inactivity
- First request after sleep will trigger a cold start (slower)
- Camera access is NOT available in browser (security restriction)
- **Face recognition will work in registration only**
- Real-time attendance with webcam requires a paid plan or local hosting

### Expected Behavior on Render:
1. ✅ Login/Authentication - Works
2. ✅ Student Registration - Works (capture face via browser)
3. ✅ View/Download Reports - Works
4. ✅ CSV/Excel Export - Works
5. ⚠️ Live Camera Feed - Limited (may not work in cloud)

### For Full Camera Support:
- Run locally: `python app.py`
- Or use a VPS with GPU support
- Or upgrade to Render Paid Plan with persistent storage

## Access Your Deployed App

Once deployed, your app will be available at:
```
https://smart-attendance-system.onrender.com
```

## Troubleshooting

### Build Errors
- Check `requirements.txt` for correct package versions
- Ensure all dependencies are compatible with Python 3.11

### Application Errors
- View logs in Render Dashboard → Logs
- Check environment variables are set
- Ensure database file permissions are correct

### Static Files Not Loading
- Verify `static/` folder is in root directory
- Check that `STATIC_URL` is not overridden

## Local Development

To run locally after testing cloud deployment:
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run the application
python app.py
```

## Security Notes

- Change default admin credentials after first login
- Username: `admin`
- Password: `admin123`

## Next Steps

1. ✅ Code pushed to GitHub
2. ⏳ Deploy to Render (follow steps above)
3. ⏳ Test all features in production
4. ⏳ Configure custom domain (optional)

---

**Repository**: https://github.com/antonyathibana/FINAL-YEAR-PROJECT
**Render Blueprint**: render.yaml included ✓

