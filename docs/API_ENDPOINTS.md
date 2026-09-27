# API Endpoints

## REST API Endpoints

### Authentication (Mock for MVP)

#### POST /api/auth/login
```json
Request:
{
  "username": "admin_01",
  "password": "password123"
}

Response:
{
  "success": true,
  "user": {
    "id": "...",
    "username": "admin_01",
    "role": "admin",
    "full_name": "Admin User"
  },
  "token": "mock_jwt_token"
}
```

#### POST /api/auth/logout
```json
Request:
{
  "token": "mock_jwt_token"
}

Response:
{
  "success": true
}
```

### Cargo Management

#### POST /api/cargo/register
```json
Request:
{
  "container_number": "MSKU-XXXXXX",
  "category": "electronics",
  "description": "Consumer electronics",
  "weight_tons": 25.5,
  "quantity": 500,
  "origin": "Gwadar Port",
  "destination": "Quetta",
  "importer_id": "...",
  "exporter_id": "...",
  "consignee": "ABC Trading Co"
}

Response:
{
  "success": true,
  "cargo_id": "GWD-2026-001284",
  "cargo": { ...cargo_object }
}
```

#### GET /api/cargo/{cargo_id}
```json
Response:
{
  "success": true,
  "cargo": { ...cargo_object }
}
```

#### GET /api/cargo
```json
Query Parameters:
- status: "registered", "verified", "in_transit", "delivered"
- destination: "Quetta"
- limit: 50
- offset: 0

Response:
{
  "success": true,
  "cargo": [...],
  "total": 1284,
  "page": 1
}
```

### Shipment Management

#### POST /api/shipments/create
```json
Request:
{
  "cargo_id": "...",
  "vehicle_id": "...",
  "driver_id": "...",
  "route_id": "...",
  "seal_number": "SEAL-12345",
  "expected_departure": "2026-09-27T10:00:00Z",
  "expected_arrival": "2026-09-27T18:00:00Z"
}

Response:
{
  "success": true,
  "shipment_id": "GWD-2026-001284",
  "qr_token": "signed_token_here",
  "shipment": { ...shipment_object }
}
```

#### GET /api/shipments/{shipment_id}
```json
Response:
{
  "success": true,
  "shipment": { ...shipment_object },
  "journey_events": [...]
}
```

#### GET /api/shipments
```json
Query Parameters:
- status: "registered", "at_port", "in_transit", "flagged", "completed"
- current_checkpoint: "CP-02"
- limit: 50
- offset: 0

Response:
{
  "success": true,
  "shipments": [...],
  "total": 342,
  "page": 1
}
```

#### PUT /api/shipments/{shipment_id}/status
```json
Request:
{
  "status": "in_transit",
  "current_checkpoint": "CP-01",
  "next_checkpoint": "CP-02"
}

Response:
{
  "success": true,
  "shipment": { ...updated_shipment }
}
```

### QR Code Operations

#### POST /api/qr/verify
```json
Request:
{
  "qr_token": "signed_token_here",
  "checkpoint_id": "CP-02",
  "officer_id": "...",
  "scanned_vehicle": "BLA-2045",
  "scanned_seal": "SEAL-12345"
}

Response:
{
  "success": true,
  "verified": true,
  "shipment": { ...shipment_object },
  "verification_details": {
    "cargo": true,
    "vehicle": true,
    "documents": true,
    "payments": true
  },
  "alerts": []
}
```

#### GET /api/qr/{cargo_id}/generate
```json
Response:
{
  "success": true,
  "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/...",
  "cargo_id": "GWD-2026-001284",
  "qr_token": "signed_token"
}
```

### Checkpoint Operations

#### POST /api/checkpoints/scan
```json
Request:
{
  "qr_token": "signed_token",
  "checkpoint_id": "CP-02",
  "officer_id": "...",
  "action": "allow" // or "hold", "report"
}

Response:
{
  "success": true,
  "event_id": "...",
  "journey_event": { ...journey_event_object }
}
```

#### GET /api/checkpoints/{checkpoint_id}/queue
```json
Response:
{
  "success": true,
  "checkpoint_id": "CP-02",
  "waiting_shipments": [...],
  "processed_today": 45
}
```

### Journey Events

#### GET /api/shipments/{shipment_id}/timeline
```json
Response:
{
  "success": true,
  "shipment_id": "GWD-2026-001284",
  "timeline": [
    {
      "event_type": "cargo_registered",
      "timestamp": "2026-09-27T09:12:00Z",
      "location": "Gwadar Port",
      "officer": "Admin",
      “status”: "success"
    },
    ...
  ]
}
```

#### POST /api/journey-events
```json
Request:
{
  "shipment_id": "...",
  "checkpoint_id": "...",
  "event_type": "checkpoint_scan",
  "officer_id": "...",
  "vehicle_id": "...",
  "seal_status": "verified",
  "verification_status": "success",
  "remarks": "All clear"
}

Response:
{
  "success": true,
  "event_id": "...",
  "journey_event": { ...journey_event_object }
}
```

### Alerts

#### GET /api/alerts
```json
Query Parameters:
- is_resolved: false
- severity: "critical"
- shipment_id: "..."

Response:
{
  "success": true,
  "alerts": [...],
  "total": 12
}
```

#### POST /api/alerts/{alert_id}/resolve
```json
Request:
{
  "resolved_by": "...",
  "remarks": "Investigated and cleared"
}

Response:
{
  "success": true,
  "alert": { ...updated_alert }
}
```

### Dashboard Metrics

#### GET /api/dashboard/metrics
```json
Response:
{
  "success": true,
  "metrics": {
    "active_shipments": 1284,
    "in_transit": 342,
    "completed_today": 86,
    "flagged": 12,
    "charges_collected_pkr": 4500000
  }
}
```

#### GET /api/dashboard/live-map
```json
Response:
{
  "success": true,
  "shipments": [
    {
      "shipment_id": "GWD-2026-001284",
      "cargo_id": "GWD-2026-001284",
      "container_number": "MSKU-XXXXXX",
      "vehicle_registration": "BLA-2045",
      "origin": "Gwadar",
      "destination": "Quetta",
      "driver_name": "Ahmed Khan",
      "current_checkpoint": "Turbat",
      "status": "in_transit",
      "seal_status": "verified",
      "next_checkpoint": "CP-03",
      "coordinates": {
        "lat": 25.1234,
        "lng": 62.5678
      },
      "marker_state": "green" // green, yellow, red, black
    }
  ]
}
```

#### GET /api/dashboard/recent-movements
```json
Response:
{
  "success": true,
  "movements": [
    {
      "cargo_id": "GWD-10284",
      "truck": "BLA-2045",
      "location": "Port Gate",
      "time": "09:42",
      "status": "Verified"
    },
    ...
  ]
}
```

### Vehicles

#### GET /api/vehicles
```json
Query Parameters:
- status: "available", "in_transit"
- registration_number: "BLA-2045"

Response:
{
  "success": true,
  "vehicles": [...]
}
```

#### POST /api/vehicles/assign
```json
Request:
{
  "vehicle_id": "...",
  "driver_id": "...",
  "shipment_id": "..."
}

Response:
{
  "success": true,
  "vehicle": { ...updated_vehicle }
}
```

### Drivers

#### GET /api/drivers
```json
Query Parameters:
- status: "active"
- license_number: "..."

Response:
{
  "success": true,
  "drivers": [...]
}
```

### Users (Admin Only)

#### GET /api/users
```json
Query Parameters:
- role: "admin", "port_officer", "checkpoint_officer", "driver"

Response:
{
  "success": true,
  "users": [...]
}
```

## WebSocket Events

### Connection
```javascript
// Client connects to
ws://localhost:8000/ws

// Server accepts connection
```

### Client → Server Messages

#### Subscribe to Shipment Updates
```json
{
  "type": "subscribe",
  "resource": "shipment",
  "shipment_id": "GWD-2026-001284"
}
```

#### Subscribe to Dashboard Updates
```json
{
  "type": "subscribe",
  "resource": "dashboard"
}
```

#### Subscribe to Checkpoint Updates
```json
{
  "type": "subscribe",
  "resource": "checkpoint",
  "checkpoint_id": "CP-02"
}
```

#### Unsubscribe
```json
{
  "type": "unsubscribe",
  "resource": "shipment",
  "shipment_id": "GWD-2026-001284"
}
```

### Server → Client Messages

#### Cargo Status Update
```json
{
  "type": "cargo_status_update",
  "data": {
    "shipment_id": "GWD-2026-001284",
    "status": "in_transit",
    "current_checkpoint": "CP-02",
    "next_checkpoint": "CP-03",
    "timestamp": "2026-09-27T13:42:00Z"
  }
}
```

#### Alert Created
```json
{
  "type": "alert_created",
  "data": {
    "alert_id": "...",
    "shipment_id": "GWD-2026-001284",
    "alert_type": "vehicle_mismatch",
    "severity": "critical",
    "message": "Vehicle mismatch detected",
    "timestamp": "2026-09-27T13:45:00Z"
  }
}
```

#### New Shipment
```json
{
  "type": "new_shipment",
  "data": {
    "shipment_id": "GWD-2026-001285",
    "cargo": { ... },
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

#### Checkpoint Scan
```json
{
  "type": "checkpoint_scan",
  "data": {
    "shipment_id": "GWD-2026-001284",
    "checkpoint_id": "CP-02",
    "verification_status": "success",
    "timestamp": "2026-09-27T13:42:00Z"
  }
}
```

#### Dashboard Metrics Update
```json
{
  "type": "dashboard_update",
  "data": {
    "active_shipments": 1285,
    "in_transit": 343,
    "completed_today": 87,
    "flagged": 12,
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

#### Live Map Update
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
    "timestamp": "2026-09-27T14:00:00Z"
  }
}
```

## Error Handling

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "vehicle_id",
      "issue": "Vehicle not found"
    }
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR` - Invalid input data
- `NOT_FOUND` - Resource not found
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Insufficient permissions
- `CONFLICT` - Resource conflict (e.g., duplicate)
- `SERVER_ERROR` - Internal server error

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error
