# Q-Route Deployment Guide 🚀

Complete step-by-step guide for deploying the Q-Route Quantum Fleet Optimization application.

> **⚠️ Important:** If deploying to Render and encountering Rust compilation errors, see [Render Deployment Issues](#render-deployment-issues) section.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Platform-Specific Deployment](#platform-specific-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)
7. [Verification](#verification)

---

## Prerequisites

### Required Software

- **Python 3.9 or higher**
  - Check version: `python --version`
  - Download: https://www.python.org/downloads/

- **Node.js 16 or higher**
  - Check version: `node --version`
  - Download: https://nodejs.org/

- **npm** (comes with Node.js)
  - Check version: `npm --version`

- **Git** (optional, for version control)
  - Check version: `git --version`
  - Download: https://git-scm.com/

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended for quantum computations)
- **Disk Space**: At least 2GB free space
- **Network**: Internet connection for OSRM routing service
- **OS**: Windows, macOS, or Linux

---

## Local Development Setup

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd QRoute

# Or download and extract the ZIP file, then navigate to the folder
cd QRoute
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**
- fastapi==0.109.0
- uvicorn==0.27.0
- qiskit==1.0.0
- qiskit-aer==0.13.3
- qiskit-optimization==0.6.0
- qiskit-algorithms==0.3.0
- numpy==1.26.3
- requests>=2.31.0
- polyline>=2.0.0
- pydantic==2.5.3
- python-multipart==0.0.6

#### 2.4 Configure Environment Variables (Optional)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file if needed (optional for local development)
# Default values work out of the box
```

#### 2.5 Start the Backend Server

```bash
python main.py
```

**Expected Output:**
```
INFO:__main__:✓ OSRM routing service is available
INFO:     Started server process [6396]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Backend is now running at:** `http://localhost:8000`

> **Note:** Keep this terminal window open. The backend must be running for the frontend to work.

### Step 3: Frontend Setup

Open a **new terminal window** (keep backend running).

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node Dependencies

```bash
npm install
```

**Expected packages:**
- react ^18.2.0
- react-dom ^18.2.0
- vite ^5.0.11
- axios ^1.13.4
- leaflet ^1.9.4
- react-leaflet ^4.2.1
- framer-motion ^11.0.3
- lucide-react ^0.312.0

#### 3.3 Start the Development Server

```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.0.11  ready in 523 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Frontend is now running at:** `http://localhost:5173`

### Step 4: Access the Application

Open your web browser and navigate to:

```
http://localhost:5173
```

You should see the Q-Route interface with an interactive map!

---

## Production Deployment

### Build for Production

#### Backend Production Build

The backend doesn't require a build step, but you should:

1. **Use a production WSGI server** (Uvicorn with workers)
2. **Set environment variables** for production
3. **Enable HTTPS** (recommended)

#### Frontend Production Build

```bash
cd frontend
npm run build
```

This creates an optimized production build in the `dist/` folder.

**Output:**
```
vite v5.0.11 building for production...
✓ 1234 modules transformed.
dist/index.html                   0.69 kB │ gzip:  0.40 kB
dist/assets/index-abc123.css     12.34 kB │ gzip:  3.21 kB
dist/assets/index-def456.js     234.56 kB │ gzip: 78.90 kB
✓ built in 5.67s
```

#### Preview Production Build Locally

```bash
npm run preview
```

Access at: `http://localhost:4173`

---

## Platform-Specific Deployment

### Option 1: Render (Recommended for Full-Stack)

#### Backend Deployment on Render

1. **Create a new Web Service** on [Render](https://render.com)

2. **Connect your repository**

3. **Configure the service:**
   - **Name:** `qroute-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

4. **Add Environment Variables:**
   ```
   HOST=0.0.0.0
   PORT=8000
   CORS_ORIGINS=https://your-frontend-url.onrender.com
   ```

5. **Deploy** and note your backend URL (e.g., `https://qroute-backend.onrender.com`)

#### Frontend Deployment on Render

1. **Create a new Static Site** on Render

2. **Configure the service:**
   - **Name:** `qroute-frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
   - **Root Directory:** `frontend`

3. **Add Environment Variable:**
   ```
   VITE_API_URL=https://qroute-backend.onrender.com
   ```

4. **Update frontend API URL** in `src/App.jsx`:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```

5. **Deploy**

### Option 2: Vercel (Frontend) + Railway (Backend)

#### Backend on Railway

1. **Create new project** on [Railway](https://railway.app)

2. **Deploy from GitHub** or upload code

3. **Configure:**
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   ```
   HOST=0.0.0.0
   PORT=$PORT
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

5. **Generate domain** and note the URL

#### Frontend on Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow prompts:**
   - Set up and deploy: `Y`
   - Scope: Select your account
   - Link to existing project: `N`
   - Project name: `qroute-frontend`
   - Directory: `./`
   - Override settings: `N`

5. **Set environment variable:**
   ```bash
   vercel env add VITE_API_URL
   # Enter your Railway backend URL
   ```

6. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Option 3: Heroku

#### Backend on Heroku

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   cd backend
   heroku create qroute-backend
   ```

4. **Create Procfile** in backend directory:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

6. **Set environment variables:**
   ```bash
   heroku config:set CORS_ORIGINS=https://your-frontend-url.herokuapp.com
   ```

#### Frontend on Heroku

1. **Create app:**
   ```bash
   cd frontend
   heroku create qroute-frontend
   ```

2. **Add buildpack:**
   ```bash
   heroku buildpacks:set heroku/nodejs
   ```

3. **Create static.json** in frontend directory:
   ```json
   {
     "root": "dist",
     "clean_urls": true,
     "routes": {
       "/**": "index.html"
     }
   }
   ```

4. **Update package.json** scripts:
   ```json
   {
     "scripts": {
       "dev": "vite",
       "build": "vite build",
       "preview": "vite preview",
       "start": "npm run preview"
     }
   }
   ```

5. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Option 4: Docker Deployment

#### Create Dockerfile for Backend

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:

```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose Setup

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - CORS_ORIGINS=http://localhost:3000
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

#### Deploy with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access at: `http://localhost:3000`

---

## Environment Configuration

### Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Origins (comma-separated)
# Development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Production (update with your actual frontend URL)
# CORS_ORIGINS=https://your-frontend-domain.com

# Optional: IBM Quantum API Token (for real quantum hardware)
# Get your token from: https://quantum-computing.ibm.com/
# IBM_QUANTUM_TOKEN=your_token_here
```

### Frontend Environment Variables

Create `.env` file in `frontend/` directory:

```env
# Backend API URL
# Development
VITE_API_URL=http://localhost:8000

# Production (update with your actual backend URL)
# VITE_API_URL=https://your-backend-domain.com
```

### Update Frontend API Configuration

Edit `frontend/src/App.jsx` to use environment variable:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

**Error:** `Address already in use`

**Solution:**
```bash
# Find and kill process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

---

#### 2. Frontend Won't Start

**Error:** `npm ERR! code ENOENT`

**Solution:**
```bash
# Delete node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

**Error:** `Failed to fetch dynamically imported module`

**Solution:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

---

#### 3. CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**

Update `backend/main.py` CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### 4. OSRM Routing Not Available

**Error:** `OSRM routing service is unavailable`

**Solution:**

This is not critical - the app will fall back to haversine distance calculations. To use real road routing:

1. **Check internet connection**
2. **Verify OSRM service is up:** Visit http://router.project-osrm.org/
3. **Wait a moment** - service may be temporarily down

---

#### 5. Quantum Computation Errors

**Error:** `Qiskit circuit execution failed`

**Solution:**
```bash
# Reinstall Qiskit packages
pip uninstall qiskit qiskit-aer qiskit-optimization qiskit-algorithms
pip install qiskit==1.0.0 qiskit-aer==0.13.3 qiskit-optimization==0.6.0 qiskit-algorithms==0.3.0
```

---

#### 6. Production Build Issues

**Error:** `Cannot find module` in production

**Solution:**

Ensure all dependencies are in `dependencies`, not `devDependencies`:

```bash
cd frontend
npm install axios leaflet react-leaflet framer-motion lucide-react --save
npm run build
```

---

#### 7. Render Deployment Issues

**Error:** Rust compilation failure on Render

```
error: failed to create directory `/usr/local/cargo/registry/cache/`
Caused by: Read-only file system (os error 30)
💥 maturin failed
```

**Root Cause:** Qiskit 1.0.0+ requires Rust compilation which fails on Render's build environment.

**Solution:**

The `requirements.txt` has been updated to use Qiskit 0.45.3 (pre-compiled wheels):

```txt
qiskit==0.45.3  # Instead of 1.0.0
scipy>=1.10.0   # Added dependency
```

**Additional Steps:**

1. **Use the provided `render.yaml`** for automatic configuration
2. **Or manually set Python version** in Render dashboard:
   - Add environment variable: `PYTHON_VERSION=3.11.0`
3. **Update build command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```

**See [`RENDER_FIX.md`](./RENDER_FIX.md) for detailed troubleshooting.**

---

## Verification

### Health Check Endpoints

#### Backend Health Check

```bash
curl http://localhost:8000/api/health
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

#### Test Optimization Endpoint

```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "locations": [
      {"lat": 28.6139, "lng": 77.2090},
      {"lat": 28.7041, "lng": 77.1025},
      {"lat": 28.5355, "lng": 77.3910}
    ],
    "num_vehicles": 2,
    "optimization_target": "distance"
  }'
```

**Expected Response:** JSON with optimized routes

### Frontend Verification

1. **Open browser:** `http://localhost:5173`
2. **Check console:** No errors (F12 → Console)
3. **Click on map:** Markers should appear
4. **Click "Optimize Routes":** Should show loading animation
5. **View results:** Routes should display on map

### Performance Benchmarks

#### Small Problem (4-6 locations)
- **Computation Time:** < 2 seconds
- **OSRM Overhead:** +0.5-1.5 seconds

#### Medium Problem (8-10 locations)
- **Computation Time:** < 5 seconds
- **OSRM Overhead:** +1-2 seconds

---

## Quick Reference Commands

### Development

```bash
# Start backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py

# Start frontend (new terminal)
cd frontend
npm run dev
```

### Production Build

```bash
# Build frontend
cd frontend
npm run build

# Preview production build
npm run preview
```

### Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Troubleshooting

```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt

# Reinstall frontend dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

---

## Security Considerations

### Production Checklist

- [ ] Update CORS origins to specific domains (not `*`)
- [ ] Use HTTPS for both frontend and backend
- [ ] Set secure environment variables (don't commit `.env`)
- [ ] Enable rate limiting on API endpoints
- [ ] Use production-grade server (Gunicorn/Nginx)
- [ ] Monitor server logs for errors
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Regular dependency updates (`npm audit`, `pip check`)

### Environment Variables Security

**Never commit these files:**
- `.env`
- `.env.local`
- `.env.production`

**Always commit:**
- `.env.example` (with placeholder values)

---

## Support and Resources

### Documentation
- [README.md](./README.md) - Project overview
- [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) - Technical details
- [PRESENTATION_SUMMARY.md](./PRESENTATION_SUMMARY.md) - Key metrics

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [OSRM Documentation](http://project-osrm.org/)

### Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review error messages** carefully
3. **Check browser console** (F12) for frontend errors
4. **Check terminal output** for backend errors
5. **Verify all prerequisites** are installed
6. **Try the troubleshooting steps** above

---

**Version:** 2.0.0  
**Last Updated:** February 2026  
**Built with ❤️ and ⚛️ Quantum Computing**
