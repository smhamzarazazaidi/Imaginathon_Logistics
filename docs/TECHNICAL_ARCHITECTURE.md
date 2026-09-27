# Technical Architecture

## System Overview

The Gwadar Smart Cargo Network is a real-time logistics tracking system built with a modern web stack. The architecture follows a client-server model with WebSocket support for real-time updates.

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Admin   │  │   Port   │  │Checkpoint │  │  Driver  │   │
│  │ Dashboard│  │  Officer │  │  Officer  │  │   App    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│                       │                                     │
│              HTTP + WebSocket                               │
└───────────────────────┼─────────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                  Backend Layer (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints  │  WebSocket Manager  │  Rules   │  │
│  └─────────────────────┴───────────────────┴────────────┘  │
│                        │                                     │
│              MongoDB Driver (Motor/PyMongo)                 │
└───────────────────────┼─────────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                  Database Layer (MongoDB)                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Cargo   │ │Shipments │ │  Users   │ │Journey   │      │
│  │          │ │          │ │          │ │  Events  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Frontend-Backend Communication Flow

### REST API Flow
1. **Client Request** → HTTP GET/POST/PUT/DELETE
2. **FastAPI Route Handler** → Process request
3. **Business Logic** → Apply rules, validate
4. **Database Query** → MongoDB operations
5. **Response** → JSON data back to client
6. **UI Update** → Render new state

### WebSocket Flow
1. **Client Connect** → WebSocket handshake
2. **Subscribe** → Client subscribes to events (e.g., cargo updates)
3. **Server Broadcast** → When cargo status changes, push to subscribers
4. **Client Update** → Real-time UI refresh without page reload

## Real-time WebSocket Architecture

### Connection Management
```python
# FastAPI WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
    except WebSocketDisconnect:
        active_connections.remove(websocket)
```

### Event Types
- `cargo_status_update` - When cargo moves between checkpoints
- `alert_created` - When rule violation detected
- `new_shipment` - When new cargo registered
- `checkpoint_scan` - When QR scanned at checkpoint

### Broadcasting Logic
```python
async def broadcast_event(event_type: str, data: dict):
    for connection in active_connections:
        await connection.send_json({
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })
```

## Database Connection Strategy

### MongoDB Connection
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
database = client.gwadar_cargo_network

# Collections
cargo_collection = database.cargo
shipments_collection = database.shipments
users_collection = database.users
journey_events_collection = database.journey_events
```

### Connection Pooling
- Motor (async MongoDB driver) handles connection pooling
- Recommended pool size: 10-100 connections
- Automatic reconnection on failure

## Deployment Architecture

### Railway Deployment
```
┌─────────────────────────────────────────┐
│           Railway App                    │
│  ┌──────────────────────────────────┐  │
│  │  FastAPI Application              │  │
│  │  - Gunicorn/Uvicorn worker       │  │
│  │  - Static file serving           │  │
│  │  - WebSocket support             │  │
│  └──────────────────────────────────┘  │
└───────────────────┬─────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
┌────────▼────────┐  ┌────────▼─────────┐
│  MongoDB Atlas  │  │  Railway Redis   │
│  (Database)     │  │  (Optional cache)│
└─────────────────┘  └──────────────────┘
```

### Environment Variables
```env
MONGODB_URL=mongodb+srv://...
RAILWAY_ENVIRONMENT=production
SECRET_KEY=your-secret-key
CORS_ORIGINS=*
```

## Security Considerations

### For MVP (Simplified)
- Mock authentication (role-based without real OAuth)
- Basic input validation
- CORS enabled for development
- No rate limiting (for demo speed)

### Production Recommendations
- JWT authentication
- Input sanitization
- Rate limiting
- HTTPS only
- Environment-specific configs
- Audit logging

## Performance Optimization

### Database Indexes
- `shipments.cargo_id` (unique)
- `journey_events.shipment_id` (indexed)
- `journey_events.timestamp` (indexed for timeline queries)
- `users.role` (indexed for role-based queries)

### Caching Strategy
- Cache active shipments in memory
- Cache checkpoint locations
- Use Redis for session management (optional for MVP)

### WebSocket Optimization
- Batch updates (send every 100ms max)
- Disconnect idle clients
- Use binary messages for large payloads
