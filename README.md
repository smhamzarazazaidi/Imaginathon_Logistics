# Gwadar Smart Cargo Network

A digital logistics and cargo verification platform for shipments moving from Gwadar Port to inland destinations. Each shipment receives a unique Cargo ID and secure QR code, with every authorized interaction recorded against that Cargo ID.

## 🚀 Quick Start

### Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Real-time**: WebSockets
- **Deployment**: Railway

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/smhamzarazazaidi/Imaginathon_Logistics.git
cd Imaginathon_Logistics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URL

# Run MongoDB (Docker)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Seed database
python scripts/seed_database.py

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Admin Dashboard: http://localhost:8000/static/admin/index.html
- Port Officer: http://localhost:8000/static/port/index.html
- Checkpoint: http://localhost:8000/static/checkpoint/index.html
- Driver App: http://localhost:8000/static/driver/index.html

## 📚 Documentation

### Core Documentation
- **[Product & UI Documentation](Gwadar_Smart_Cargo_Network_Documentation.md)** - Complete product specification, user roles, and UI requirements
- **[Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)** - System overview, WebSocket architecture, deployment architecture
- **[Database Schema](docs/DATABASE_SCHEMA.md)** - MongoDB collections, schemas, relationships, and sample data
- **[API Endpoints](docs/API_ENDPOINTS.md)** - REST API routes, WebSocket events, request/response formats

### Implementation Guides
- **[UI/UX Design System](docs/UI_UX_DESIGN_SYSTEM.md)** - Color palette, typography, component specifications, layout patterns
- **[Component Structure](docs/COMPONENT_STRUCTURE.md)** - Frontend file organization, reusable components, page breakdown
- **[Real-time Architecture](docs/REALTIME_ARCHITECTURE.md)** - WebSocket management, event patterns, broadcasting logic
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Railway setup, MongoDB configuration, environment variables

### Execution Plan
- **[Master Roadmap](docs/MASTER_ROADMAP.md)** - 4-hour execution timeline, team roles, phase breakdown, demo script

## 🎯 Core Features

### User Roles
- **Admin/Control Room** - Monitor entire logistics network with live map and alerts
- **Port/Gate Officer** - Register and release cargo from port
- **Checkpoint Officer** - Verify trucks and cargo while traveling
- **Driver** - Carry digital shipment credentials and view journey requirements

### Key Capabilities
- ✅ Unique Cargo ID generation with secure QR codes
- ✅ Real-time cargo tracking with live map
- ✅ Rule-based verification (no AI required)
- ✅ Complete journey timeline and audit trail
- ✅ Alert system for violations (vehicle mismatch, seal mismatch, etc.)
- ✅ Role-based access control
- ✅ WebSocket real-time updates

## 🔄 Core Flow

```
Cargo Registered → Documents Verified → Truck Assigned → QR Issued → 
Port Gate Scan → Checkpoints → Destination Verification → Journey Closed
```

## 🎨 UI Design

**Design Philosophy**: Port Command Center + Modern Infrastructure System

- Dark navy sidebar with white/light-gray workspace
- Information-dense but clean layout
- Green verification states, amber warnings, red critical alerts
- Minimal rounded corners, strong typography
- Mobile-first checkpoint interface with large scanner buttons

## 📊 Demo Scenario

1. **Register Cargo** - Admin registers shipment and generates QR
2. **Port Clearance** - Port officer scans QR, verifies, clears for exit
3. **Begin Journey** - Truck appears on admin dashboard as "IN TRANSIT"
4. **Checkpoint Verification** - Checkpoint officer scans QR, verifies
5. **Simulate Violation** - Modify truck number, trigger alert, show resolution

**Demo Time**: 7 minutes

## 🛠️ Development

### Project Structure
```
Imaginathon_Logistics/
├── backend/              # FastAPI application
│   ├── main.py          # Entry point
│   ├── api/             # API routers
│   ├── models/          # Pydantic models
│   └── websocket/       # WebSocket handlers
├── frontend/            # HTML/CSS/JS
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── assets/          # Images, icons
├── docs/                # Documentation
├── scripts/             # Utility scripts
└── requirements.txt     # Python dependencies
```

### Testing API
```bash
# Health check
curl http://localhost:8000/health

# Register cargo
curl -X POST http://localhost:8000/api/cargo/register \
  -H "Content-Type: application/json" \
  -d '{"container_number": "MSKU-001", "category": "electronics"}'

# Get dashboard metrics
curl http://localhost:8000/api/dashboard/metrics
```

## 🚢 Deployment

### Railway Deployment
See [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

```bash
# Deploy to Railway
railway up
```

### Environment Variables
```env
MONGODB_URL=mongodb+srv://...
SECRET_KEY=your-secret-key
CORS_ORIGINS=*
ENVIRONMENT=production
```

## 🤝 Contributing

This is a hackathon project. For contributions:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 👥 Team

- **Backend**: FastAPI, MongoDB, WebSocket
- **Frontend**: HTML/CSS/JS, Real-time UI
- **Design**: Port Command Center aesthetic

## 🎯 MVP Timeline

**4-Hour Execution Plan** - See [Master Roadmap](docs/MASTER_ROADMAP.md)

- Phase 1: Setup & Infrastructure (30 min)
- Phase 2: Backend Core (60 min)
- Phase 3: Frontend Core (90 min)
- Phase 4: Real-time Integration (30 min)
- Phase 5: Polish & Demo (30 min)

## 📞 Support

For questions or issues:
- Review documentation in `/docs`
- Check API docs at `/docs` endpoint
- Open an issue on GitHub

---

**Core Pitch**: *"We aren't just digitizing a container. We're creating a verifiable digital journey from Gwadar Port to its destination."*

The core innovation is a **connected cargo identity, verification network, and auditable chain of custody** across Gwadar's port-to-road logistics journey.
