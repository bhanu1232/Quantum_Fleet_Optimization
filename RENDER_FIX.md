# Render Deployment Fix Guide

## Problem: Rust Compilation Error

**Error Message:**
```
error: failed to create directory `/usr/local/cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`
Caused by: Read-only file system (os error 30)
💥 maturin failed
```

**Root Cause:** Qiskit 1.0.0+ requires Rust compilation, which fails on Render's build environment due to filesystem restrictions.

---

## ✅ Solution Applied

### 1. Updated `requirements.txt`

**Changed:**
```diff
- qiskit==1.0.0
+ qiskit==0.45.3
+ scipy>=1.10.0
```

**Why:** Qiskit 0.45.3 uses pre-compiled wheels that don't require Rust compilation.

### 2. Created `render.yaml`

Added automatic deployment configuration with:
- Python 3.11 (stable and compatible)
- Correct build and start commands
- Environment variables pre-configured

---

## 🚀 Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Commit the changes:**
   ```bash
   git add .
   git commit -m "Fix: Use Qiskit 0.45.3 for Render compatibility"
   git push origin main
   ```

2. **In Render Dashboard:**
   - Click "New" → "Blueprint"
   - Connect your repository
   - Render will automatically detect `render.yaml`
   - Click "Apply"

### Option 2: Manual Configuration

If you already created the service manually:

1. **Update Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```

2. **Add Environment Variable:**
   - Go to your service settings
   - Add: `PYTHON_VERSION` = `3.11.0`

3. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🔍 Verification

After deployment completes:

1. **Check Build Logs** - Should see:
   ```
   Successfully installed qiskit-0.45.3 ...
   Build succeeded 🎉
   ```

2. **Test Health Endpoint:**
   ```bash
   curl https://your-service-name.onrender.com/api/health
   ```

   **Expected Response:**
   ```json
   {
     "status": "healthy",
     "quantum_backend": "AerSimulator",
     "algorithm": "QAOA-inspired",
     "routing_service": "OSRM",
     "real_roads_available": true
   }
   ```

---

## 🎯 Next Steps

1. **Update Frontend:**
   - Set `VITE_API_URL` to your Render backend URL
   - Deploy frontend to Render/Vercel

2. **Update CORS:**
   - In Render dashboard, update `CORS_ORIGINS` environment variable
   - Add your frontend URL: `https://your-frontend.onrender.com`

3. **Test Full Application:**
   - Open frontend
   - Add locations on map
   - Click "Optimize Routes"
   - Verify routes display correctly

---

## 🆘 Still Having Issues?

### If build still fails:

**Try Python 3.10:**
```yaml
# In render.yaml
envVars:
  - key: PYTHON_VERSION
    value: 3.10.0
```

**Or use Docker deployment:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### If quantum computations fail:

Check that all Qiskit packages are compatible:
```bash
pip list | grep qiskit
```

Should show:
```
qiskit                0.45.3
qiskit-aer            0.13.3
qiskit-algorithms     0.3.0
qiskit-optimization   0.6.0
```

---

## 📊 Performance Notes

**Qiskit 0.45.3 vs 1.0.0:**
- ✅ Same quantum algorithm performance
- ✅ Compatible with all Q-Route features
- ✅ No breaking changes for our use case
- ✅ Faster deployment (no compilation needed)

The downgrade is purely for deployment compatibility and does not affect application functionality.

---

**Last Updated:** February 2026
