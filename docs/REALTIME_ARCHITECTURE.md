# Real-time Architecture

## WebSocket Connection Management

### Server-Side Implementation (FastAPI)

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set, Dict
import json

class ConnectionManager:
    def __init__(self):
        # Active connections
        self.active_connections: Set[WebSocket] = set()
        
        # Subscriptions by resource type
        self.subscriptions: Dict[str, Set[WebSocket]] = {
            'dashboard': set(),
            'shipment': set(),
            'checkpoint': set()
        }
        
        # Resource-specific subscriptions
        self.resource_subscriptions: Dict[str, Dict[str, Set[WebSocket]]] = {
            'shipment': {},  # shipment_id -> set of connections
            'checkpoint': {}  # checkpoint_id -> set of connections
        }

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
        # Remove from all subscriptions
        for resource_type in self.subscriptions:
            if websocket in self.subscriptions[resource_type]:
                self.subscriptions[resource_type].remove(websocket)
        
        for resource_type in self.resource_subscriptions:
            for resource_id, connections in self.resource_subscriptions[resource_type].items():
                if websocket in connections:
                    connections.remove(websocket)

    async def subscribe(self, websocket: WebSocket, resource: str, resource_id: str = None):
        if resource in self.subscriptions:
            self.subscriptions[resource].add(websocket)
        
        if resource_id and resource in self.resource_subscriptions:
            if resource_id not in self.resource_subscriptions[resource]:
                self.resource_subscriptions[resource][resource_id] = set()
            self.resource_subscriptions[resource][resource_id].add(websocket)

    async def unsubscribe(self, websocket: WebSocket, resource: str, resource_id: str = None):
        if resource in self.subscriptions and websocket in self.subscriptions[resource]:
            self.subscriptions[resource].remove(websocket)
        
        if resource_id and resource in self.resource_subscriptions:
            if resource_id in self.resource_subscriptions[resource]:
                self.resource_subscriptions[resource][resource_id].discard(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

    async def broadcast_to_resource(self, resource: str, message: dict):
        if resource in self.subscriptions:
            for connection in self.subscriptions[resource]:
                try:
                    await connection.send_json(message)
                except:
                    self.disconnect(connection)

    async def broadcast_to_resource_id(self, resource: str, resource_id: str, message: dict):
        if resource in self.resource_subscriptions:
            if resource_id in self.resource_subscriptions[resource]:
                for connection in self.resource_subscriptions[resource][resource_id]:
                    try:
                        await connection.send_json(message)
                    except:
                        self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle client messages
            if message.get('type') == 'subscribe':
                await manager.subscribe(
                    websocket,
                    message.get('resource'),
                    message.get('resource_id')
                )
            elif message.get('type') == 'unsubscribe':
                await manager.unsubscribe(
                    websocket,
                    message.get('resource'),
                    message.get('resource_id')
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Client-Side Implementation

```javascript
// js/websocket.js
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectInterval = 5000;
    this.maxReconnectAttempts = 10;
    this.reconnectAttempts = 0;
    this.subscriptions = new Set();
    this.eventHandlers = {};
    this.heartbeatInterval = null;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.startHeartbeat();
      this.resubscribe();
      this.emit('connected');
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.stopHeartbeat();
      this.emit('disconnected');
      
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
        setTimeout(() => this.connect(), this.reconnectInterval);
      }
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.stopHeartbeat();
  }

  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'heartbeat' }));
      }
    }, 30000); // 30 seconds
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  subscribe(resource, resourceId = null) {
    const subscription = { resource, resourceId };
    this.subscriptions.add(subscription);
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        resource,
        resource_id: resourceId
      }));
    }
  }

  unsubscribe(resource, resourceId = null) {
    const subscription = { resource, resourceId };
    this.subscriptions.delete(subscription);
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'unsubscribe',
        resource,
        resource_id: resourceId
      }));
    }
  }

  resubscribe() {
    this.subscriptions.forEach(({ resource, resourceId }) => {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        resource,
        resource_id: resourceId
      }));
    });
  }

  on(event, handler) {
    if (!this.eventHandlers[event]) {
      this.eventHandlers[event] = [];
    }
    this.eventHandlers[event].push(handler);
  }

  off(event, handler) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event] = this.eventHandlers[event].filter(h => h !== handler);
    }
  }

  emit(event, data) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event].forEach(handler => handler(data));
    }
  }

  handleMessage(message) {
    const { type, data } = message;
    
    // Emit specific event
    this.emit(type, data);
    
    // Also emit generic message event
    this.emit('message', message);
  }
}

// Usage
const ws = new WebSocketClient('ws://localhost:8000/ws');
ws.connect();

ws.on('cargo_status_update', (data) => {
  console.log('Cargo status updated:', data);
  // Update UI
});

ws.on('alert_created', (data) => {
  console.log('New alert:', data);
  // Show alert notification
});

ws.subscribe('dashboard');
ws.subscribe('shipment', 'GWD-2026-001284');
```

## Event Types and Payloads

### Cargo Status Update
```json
{
  "type": "cargo_status_update",
  "data": {
    "shipment_id": "GWD-2026-001284",
    "cargo_id": "GWD-2026-001284",
    "status": "in_transit",
    "current_checkpoint": "CP-02",
    "next_checkpoint": "CP-03",
    "timestamp": "2026-09-27T13:42:00Z",
    "coordinates": {
      "lat": 25.1234,
      "lng": 62.5678
    }
  }
}
```

**Triggered when:**
- Cargo moves between checkpoints
- Status changes (registered → in_transit → completed)
- Checkpoint scan successful

### Alert Created
```json
{
  "type": "alert_created",
  "data": {
    "alert_id": "alert_123",
    "shipment_id": "GWD-2026-001284",
    "alert_type": "vehicle_mismatch",
    "severity": "critical",
    "message": "Vehicle mismatch detected at CP-02",
    "checkpoint_id": "CP-02",
    "timestamp": "2026-09-27T13:45:00Z"
  }
}
```

**Triggered when:**
- Rule engine detects violation
- Vehicle mismatch
- Seal mismatch
- Checkpoint sequence violation
- Permit expired
- Payment pending

### New Shipment
```json
{
  "type": "new_shipment",
  "data": {
    "shipment_id": "GWD-2026-001285",
    "cargo_id": "GWD-2026-001285",
    "container_number": "MSKU-YYYYYY",
    "vehicle_registration": "BLA-2046",
    "origin": "Gwadar",
    "destination": "Quetta",
    "status": "registered",
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

**Triggered when:**
- New cargo registered
- New shipment created

### Checkpoint Scan
```json
{
  "type": "checkpoint_scan",
  "data": {
    "shipment_id": "GWD-2026-001284",
    "checkpoint_id": "CP-02",
    "officer_id": "officer_01",
    "verification_status": "success",
    "seal_status": "verified",
    "timestamp": "2026-09-27T13:42:00Z"
  }
}
```

**Triggered when:**
- QR scanned at checkpoint
- Verification completed

### Dashboard Metrics Update
```json
{
  "type": "dashboard_update",
  "data": {
    "active_shipments": 1285,
    "in_transit": 343,
    "completed_today": 87,
    "flagged": 12,
    "charges_collected_pkr": 4550000,
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

**Triggered when:**
- Shipment status changes
- New shipment created
- Shipment completed
- Alert created/resolved

### Live Map Update
```json
{
  "type": "map_update",
  "data": {
    "shipment_id": "GWD-2026-001284",
    "coordinates": {
      "lat": 25.1234,
      "lng": 62.5678
    },
    "marker_state": "green",
    "current_checkpoint": "CP-02",
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

**Triggered when:**
- Cargo location changes
- Status changes (affects marker color)

### Alert Resolved
```json
{
  "type": "alert_resolved",
  "data": {
    "alert_id": "alert_123",
    "shipment_id": "GWD-2026-001284",
    "resolved_by": "admin_01",
    "resolved_at": "2026-09-27T14:10:00Z",
    "remarks": "Investigated and cleared",
    "timestamp": "2026-09-27T14:10:00Z"
  }
}
```

**Triggered when:**
- Admin resolves alert

## Client-Side Subscription Patterns

### Subscribe to Dashboard Updates
```javascript
// Admin dashboard
ws.subscribe('dashboard');

ws.on('dashboard_update', (data) => {
  updateMetricCards(data);
});

ws.on('new_shipment', (data) => {
  addShipmentToLiveMap(data);
});

ws.on('alert_created', (data) => {
  showAlertNotification(data);
});
```

### Subscribe to Specific Shipment
```javascript
// Shipment detail view
const shipmentId = 'GWD-2026-001284';
ws.subscribe('shipment', shipmentId);

ws.on('cargo_status_update', (data) => {
  if (data.shipment_id === shipmentId) {
    updateShipmentStatus(data);
  }
});

ws.on('checkpoint_scan', (data) => {
  if (data.shipment_id === shipmentId) {
    addTimelineEvent(data);
  }
});
```

### Subscribe to Checkpoint Updates
```javascript
// Checkpoint officer view
const checkpointId = 'CP-02';
ws.subscribe('checkpoint', checkpointId);

ws.on('checkpoint_scan', (data) => {
  if (data.checkpoint_id === checkpointId) {
    showScanResult(data);
  }
});
```

## Server-Side Broadcasting Logic

### Broadcasting Functions

```python
async def broadcast_cargo_update(shipment_id: str, status: str, current_checkpoint: str, next_checkpoint: str):
    message = {
        "type": "cargo_status_update",
        "data": {
            "shipment_id": shipment_id,
            "status": status,
            "current_checkpoint": current_checkpoint,
            "next_checkpoint": next_checkpoint,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    # Broadcast to dashboard subscribers
    await manager.broadcast_to_resource('dashboard', message)
    
    # Broadcast to specific shipment subscribers
    await manager.broadcast_to_resource_id('shipment', shipment_id, message)

async def broadcast_alert(alert: dict):
    message = {
        "type": "alert_created",
        "data": alert
    }
    
    # Broadcast to dashboard subscribers
    await manager.broadcast_to_resource('dashboard', message)
    
    # Broadcast to specific shipment subscribers
    await manager.broadcast_to_resource_id('shipment', alert['shipment_id'], message)
    
    # Broadcast to checkpoint subscribers
    if 'checkpoint_id' in alert:
        await manager.broadcast_to_resource_id('checkpoint', alert['checkpoint_id'], message)

async def broadcast_dashboard_metrics(metrics: dict):
    message = {
        "type": "dashboard_update",
        "data": metrics
    }
    
    await manager.broadcast_to_resource('dashboard', message)

async def broadcast_map_update(shipment_id: str, coordinates: dict, marker_state: str):
    message = {
        "type": "map_update",
        "data": {
            "shipment_id": shipment_id,
            "coordinates": coordinates,
            "marker_state": marker_state,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    await manager.broadcast_to_resource('dashboard', message)
```

### Integration with API Endpoints

```python
@app.post("/api/checkpoints/scan")
async def checkpoint_scan(scan_data: CheckpointScan):
    # Process scan
    result = await process_checkpoint_scan(scan_data)
    
    # Create journey event
    journey_event = await create_journey_event(result)
    
    # Broadcast to subscribers
    await broadcast_cargo_update(
        shipment_id=scan_data.shipment_id,
        status=result.status,
        current_checkpoint=scan_data.checkpoint_id,
        next_checkpoint=result.next_checkpoint
    )
    
    # If alert created, broadcast it
    if result.alert:
        await broadcast_alert(result.alert)
    
    return result

@app.post("/api/cargo/register")
async def register_cargo(cargo_data: CargoRegistration):
    # Register cargo
    cargo = await register_new_cargo(cargo_data)
    
    # Broadcast new shipment
    message = {
        "type": "new_shipment",
        "data": cargo
    }
    await manager.broadcast_to_resource('dashboard', message)
    
    # Update dashboard metrics
    metrics = await calculate_dashboard_metrics()
    await broadcast_dashboard_metrics(metrics)
    
    return cargo
```

## Reconnection Strategy

### Exponential Backoff
```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.reconnectDelay = 1000; // Start with 1 second
    this.maxReconnectDelay = 30000; // Max 30 seconds
    this.reconnectAttempts = 0;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onclose = () => {
      console.log(`Disconnected. Reconnecting in ${this.reconnectDelay}ms...`);
      
      setTimeout(() => {
        this.connect();
        this.reconnectDelay = Math.min(
          this.reconnectDelay * 2,
          this.maxReconnectDelay
        );
        this.reconnectAttempts++;
      }, this.reconnectDelay);
    };
    
    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectDelay = 1000; // Reset delay
      this.reconnectAttempts = 0;
      this.resubscribe();
    };
  }
}
```

### Connection Health Check
```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.lastMessageTime = null;
    this.healthCheckInterval = null;
  }

  startHealthCheck() {
    this.healthCheckInterval = setInterval(() => {
      const timeSinceLastMessage = Date.now() - this.lastMessageTime;
      
      // If no message for 60 seconds, consider connection dead
      if (timeSinceLastMessage > 60000) {
        console.warn('Connection appears dead, reconnecting...');
        this.disconnect();
        this.connect();
      }
    }, 30000); // Check every 30 seconds
  }

  handleMessage(message) {
    this.lastMessageTime = Date.now();
    // Process message...
  }
}
```

## Performance Optimization

### Batching Updates
```python
from collections import defaultdict
import asyncio

class UpdateBatcher:
    def __init__(self, manager: ConnectionManager, batch_interval: float = 0.1):
        self.manager = manager
        self.batch_interval = batch_interval
        self.batches = defaultdict(list)
        self.batch_tasks = {}

    async def queue_update(self, resource: str, message: dict):
        self.batches[resource].append(message)
        
        if resource not in self.batch_tasks:
            self.batch_tasks[resource] = asyncio.create_task(
                self._flush_batch(resource)
            )

    async def _flush_batch(self, resource: str):
        await asyncio.sleep(self.batch_interval)
        
        if self.batches[resource]:
            # Send all updates as a single message
            batched_message = {
                "type": "batched_updates",
                "resource": resource,
                "updates": self.batches[resource]
            }
            await self.manager.broadcast_to_resource(resource, batched_message)
            self.batches[resource].clear()
        
        del self.batch_tasks[resource]

batcher = UpdateBatcher(manager)

# Instead of immediate broadcast
await batcher.queue_update('dashboard', message)
```

### Message Compression
```python
import gzip
import json

async def send_compressed(websocket: WebSocket, message: dict):
    json_str = json.dumps(message)
    compressed = gzip.compress(json_str.encode())
    await websocket.send_bytes(compressed)
```

### Selective Broadcasting
```python
async def broadcast_to_relevant_users(message: dict, user_roles: list):
    for connection in manager.active_connections:
        # Check if connection's user role is in target roles
        if connection.user_role in user_roles:
            await connection.send_json(message)
```

## Security Considerations

### Authentication
```python
@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Verify token
    user = await verify_token(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    await manager.connect(websocket)
    websocket.user = user
    websocket.user_role = user.role
    
    try:
        while True:
            data = await websocket.receive_text()
            # Handle message
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Rate Limiting
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_messages: int = 100, window: int = 60):
        self.max_messages = max_messages
        self.window = window
        self.message_counts = defaultdict(list)

    def can_send(self, connection_id: str) -> bool:
        now = time.time()
        
        # Clean old messages
        self.message_counts[connection_id] = [
            t for t in self.message_counts[connection_id]
            if now - t < self.window
        ]
        
        # Check limit
        if len(self.message_counts[connection_id]) >= self.max_messages:
            return False
        
        self.message_counts[connection_id].append(now)
        return True

rate_limiter = RateLimiter()
```

### Message Validation
```python
def validate_websocket_message(message: dict) -> bool:
    required_fields = ['type', 'data']
    
    for field in required_fields:
        if field not in message:
            return False
    
    # Validate message type
    valid_types = ['subscribe', 'unsubscribe', 'heartbeat']
    if message['type'] not in valid_types:
        return False
    
    return True
```
