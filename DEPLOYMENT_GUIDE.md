# Deployment Guide - Render.com

## Issues Fixed

### 1. **Static Files Collection Error**
   - **Problem**: `CompressedManifestStaticFilesStorage` was failing during deployment
   - **Solution**: Changed to `WhiteNoiseStaticFilesStorage` for simpler, more reliable handling
   - **Setting**: `STATICFILES_STORAGE = 'whitenoise.storage.WhiteNoiseStaticFilesStorage'`

### 2. **Build Command Conflict**
   - **Problem**: `collectstatic --noinput` was causing file deletion errors
   - **Solution**: Removed from build command, rely on `DISABLE_COLLECTSTATIC=1` environment variable
   - **Result**: Static files are served directly by WhiteNoise from the app bundle

### 3. **Environment Variables**
   - **Problem**: Missing critical environment variables
   - **Solution**: Added to `render.yaml`:
     - `DISABLE_COLLECTSTATIC=1` - Prevents automatic collection
     - `PYTHONUNBUFFERED=1` - Ensures real-time logging
     - `DEBUG=False` - Production security setting

### 4. **Procfile Configuration**
   - **Updated**: Migration command with `--no-input` flag
   - **Added**: Gunicorn logging and worker configuration for better performance

## Pre-Deployment Checklist

Before pushing to Render, ensure:

1. ✅ **Environment Variables Set in Render Dashboard**:
   ```
   DEBUG = False
   DISABLE_COLLECTSTATIC = 1
   PYTHONUNBUFFERED = 1
   SECRET_KEY = [your-secret-key]
   DATABASE_URL = [your-postgresql-url]
   ```

2. ✅ **Git Repository Clean**:
   ```bash
   git status
   # Should not include __pycache__, *.pyc, db.sqlite3, media/
   ```

3. ✅ **Run Local Verification**:
   ```bash
   python check_deployment.py
   ```

## Deployment Steps

1. **Commit Changes**:
   ```bash
   git add -A
   git commit -m "Fix deployment configuration"
   git push origin main
   ```

2. **Monitor Deployment** on Render Dashboard:
   - Check logs for errors
   - Wait for "Live" status (typically 2-3 minutes)

3. **Verify Application**:
   - Access your deployed URL
   - Check static files load (CSS, JS, images)
   - Verify database migrations ran

## Troubleshooting

### Static Files Not Loading
- Ensure `DISABLE_COLLECTSTATIC=1` is set
- Check that WhiteNoise middleware is enabled
- Clear browser cache

### Database Connection Errors
- Verify `DATABASE_URL` environment variable is set
- Ensure PostgreSQL database is created and accessible
- Check credentials in connection string

### Application Won't Start
- Check Render logs for specific errors
- Verify all required packages in `requirements.txt`
- Ensure `SECRET_KEY` environment variable is set

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DEBUG=False
export DISABLE_COLLECTSTATIC=1
export SECRET_KEY='your-test-key'
export DATABASE_URL='sqlite:///db.sqlite3'

# Run migrations
python manage.py migrate

# Collect static files (optional, WhiteNoise handles this)
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```
