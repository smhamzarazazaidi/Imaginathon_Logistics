# Deployment Guide

## Railway Deployment

### Prerequisites
- Railway account (free tier available)
- MongoDB Atlas account (free tier available)
- Git repository with project code
- Python 3.9+ installed locally

### Step 1: MongoDB Atlas Setup

1. **Create MongoDB Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up for free account
   - Create a new project: "Gwadar Cargo Network"

2. **Create Cluster**
   - Click "Build a Cluster"
   - Select "M0 Sandbox" (free tier)
   - Choose region closest to your users (e.g., Singapore for Pakistan)
   - Cluster name: "gwadar-cluster"
   - Click "Create Cluster"

3. **Create Database User**
   - Go to "Database Access" → "Add New Database User"
   - Username: `gwadar_admin`
   - Password: (generate strong password)
   - Database User Privileges: "Read and write to any database"
   - Click "Add User"

4. **Network Access**
   - Go to "Network Access" → "Add IP Address"
   - For development: "Allow Access from Anywhere" (0.0.0.0/0)
   - For production: Add Railway's IP ranges

5. **Get Connection String**
   - Go to "Clusters" → Click "Connect"
   - Select "/drivers"
   - Select "Python"
   - Copy connection string
   - Replace `<password>` with your database user password
   - Example: `mongodb+srv://gwadar_admin:password@gwadar-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority`

### Step 2: Railway Setup

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub
   - Verify email

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `Imaginathon_Logistics`
   - Railway will analyze your repository

3. **Add MongoDB Service**
   - In your Railway project, click "New Service"
   - Select "Database"
   - Choose "MongoDB"
   - Railway will create a MongoDB instance
   - Copy the MongoDB connection URL from Railway (or use Atlas)

4. **Add FastAPI Service**
   - Click "New Service"
   - Select "GitHub Repo"
   - Select your repository
   - Railway will detect Python project

### Step 3: Project Configuration

#### Create `requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
motor==3.3.2
pymongo==4.6.0
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
websockets==12.0
python-multipart==0.0.6
```

#### Create `main.py` (FastAPI Entry Point)
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Gwadar Cargo Network API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
# from api import cargo, shipments, checkpoints, dashboard
# app.include_router(cargo.router)
# app.include_router(shipments.router)
# app.include_router(checkpoints.router)
# app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "Gwadar Cargo Network API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Create `.env` file (local development)
```env
MONGODB_URL=mongodb+srv://gwadar_admin:password@gwadar-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here-change-in-production
CORS_ORIGINS=*
ENVIRONMENT=development
```

#### Create `railway.env` (Railway environment variables)
In Railway dashboard, go to your FastAPI service → Variables → Add Variable:

```env
MONGODB_URL=${{MONGODB_URL}}
SECRET_KEY=${{SECRET_KEY}}
CORS_ORIGINS=*
ENVIRONMENT=production
PORT=8000
```

### Step 4: Railway Build Configuration

#### Create `railway.toml` (optional, for custom build)
```toml
[build]
builder = "NIXPACKS"

[build.env]
PYTHON_VERSION = "3.11"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
```

#### Or use `Procfile` (simpler)
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Deploy to Railway

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Railway Auto-Deploy**
   - Railway will automatically detect new commits
   - Build process will start
   - Monitor build logs in Railway dashboard

3. **Check Deployment**
   - Go to Railway dashboard → Your service
   - Click the generated URL (e.g., `https://gwadar-cargo.up.railway.app`)
   - Test health endpoint: `https://gwadar-cargo.up.railway.app/health`

4. **Configure Domain (Optional)**
   - Go to Settings → Domains
   - Add custom domain (e.g., `cargo.gwadar.pk`)
   - Update DNS records as instructed

### Step 6: Verify Deployment

```bash
# Test API endpoints
curl https://your-app.up.railway.app/health
curl https://your-app.up.railway.app/

# Test WebSocket connection
wscat -c wss://your-app.up.railway.app/ws
```

## Local Development Setup

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/smhamzarazazaidi/Imaginathon_Logistics.git
cd Imaginathon_Logistics
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your MongoDB URL
# MONGODB_URL=mongodb+srv://...
```

### Step 5: Run MongoDB (Local)
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
# Follow: https://www.mongodb.com/docs/manual/installation/
```

### Step 6: Seed Database (Optional)
```bash
python scripts/seed_database.py
```

### Step 7: Run Development Server
```bash
# Run FastAPI with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python main.py
```

### Step 8: Access Application
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:8000/static/index.html

## Environment Variables

### Required Variables
```env
MONGODB_URL          # MongoDB connection string
SECRET_KEY           # JWT secret key (for future auth)
```

### Optional Variables
```env
CORS_ORIGINS         # Allowed CORS origins (default: *)
ENVIRONMENT          # development/production (default: development)
PORT                 # Server port (default: 8000)
LOG_LEVEL            # logging level (default: INFO)
```

## Database Migration Strategy

### For MVP (No Migrations)
- Use MongoDB schemaless design
- Application handles schema changes
- Seed data with scripts

### For Production (Future)
```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migration
alembic upgrade head
```

## Monitoring & Logging

### Railway Built-in Monitoring
- View logs in Railway dashboard
- Metrics available in service dashboard
- Health checks configured in `railway.toml`

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello"}
```

### Error Tracking (Optional)
```bash
# Install Sentry
pip install sentry-sdk

# Add to main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

## Performance Optimization

### Enable Compression
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Enable Caching (Future)
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

redis = aioredis.from_url("redis://localhost")
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### Database Indexing
```python
# Create indexes on startup
@app.on_event("startup")
async def startup_db_client():
    await db.cargo.create_index([("cargo_id", 1)], unique=True)
    await db.shipments.create_index([("status", 1)])
    await db.journey_events.create_index([("shipment_id", 1), ("timestamp", -1)])
```

## Security Checklist

### Before Production Deployment
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Restrict `CORS_ORIGINS` to specific domains
- [ ] Enable HTTPS (Railway provides this automatically)
- [ ] Implement proper authentication (JWT)
- [ ] Add rate limiting
- [ ] Sanitize all user inputs
- [ ] Enable request validation
- [ ] Add API versioning
- [ ] Implement proper error handling
- [ ] Add audit logging
- [ ] Regular security updates

### Railway-Specific Security
- [ ] Enable Railway's built-in secrets management
- [ ] Use Railway's private networking for database
- [ ] Enable Railway's automatic backups
- [ ] Configure Railway's access controls

## Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check MongoDB URL format
# Ensure IP whitelist includes Railway's IPs
# Check database user credentials
```

#### Build Fails on Railway
```bash
# Check requirements.txt for correct versions
# Ensure Python version is compatible
# Check build logs for specific errors
```

#### WebSocket Connection Fails
```bash
# Check if WebSocket endpoint is accessible
# Verify CORS configuration
# Check firewall settings
 ensure Railway supports WebSocket (it does)
```

#### Static Files Not Loading
```python
# Ensure static files are mounted correctly
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Check file paths in HTML
<script src="/static/js/main.js"></script>
```

### Railway Logs Access
```bash
# View logs in Railway dashboard
# Or use Railway CLI
railway logs

# Follow logs
railway logs --follow
```

### Database Connection Issues
```python
# Add connection retry logic
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def get_database():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = AsyncIOMotorClient(MONGODB_URL)
            return client.gwadar_cargo_network
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

## Backup Strategy

### MongoDB Atlas Backup
- Atlas provides automatic backups (paid tiers)
- For free tier: manual exports
```bash
# Export database
mongodump --uri="mongodb+srv://..." --out=./backup

# Import database
mongorestore --uri="mongodb+srv://..." ./backup
```

### Railway Backup
- Railway provides automatic backups
- Manual snapshots available in dashboard
- Export data regularly

## Scaling Considerations

### When to Scale
- API response time > 500ms
- Database connections near limit
- WebSocket connections > 1000
- Memory usage > 80%

### Scaling Options
1. **Vertical Scaling**: Increase Railway plan resources
2. **Horizontal Scaling**: Add more Railway services with load balancer
3. **Database Scaling**: Upgrade MongoDB Atlas tier
4. **CDN**: Use Cloudflare for static assets

## Cost Estimation

### Railway (MVP)
- Free tier: $0/month (512MB RAM, 0.5vCPU)
- Basic tier: $5/month (1GB RAM, 1vCPU)
- Pro tier: $20/month (2GB RAM, 2vCPU)

### MongoDB Atlas
- Free tier (M0): $0/month (512MB storage)
- Basic tier (M2): $9/month (2GB storage)
- Production tier (M10): $57/month (10GB storage)

### Total MVP Cost
- Railway Free + Atlas Free = $0/month
- Railway Basic + Atlas Basic = $14/month

## CI/CD Pipeline (Optional)

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railwayapp/cli-action@v1.0.0
        with:
          railway-token: ${{ secrets.RAILWAY_TOKEN }}
          service: your-service-id
```

## Rollback Strategy

### Railway Rollback
1. Go to Railway dashboard
2. Select service
3. Click "Deployments"
4. Select previous deployment
5. Click "Redeploy"

### Database Rollback
```bash
# Restore from backup
mongorestore --uri="mongodb+srv://..." ./backup/timestamp
```

## Support Resources

- Railway Documentation: https://docs.railway.app
- MongoDB Atlas Documentation: https://docs.atlas.mongodb.com
- FastAPI Documentation: https://fastapi.tiangolo.com
- Motor (Async MongoDB): https://motor.readthedocs.io
