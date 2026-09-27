# Database Schema

## MongoDB Collections Overview

```javascript
Collections:
- users
- organizations
- drivers
- vehicles
- containers
- cargo
- shipments
- routes
- checkpoints
- journey_events (CRITICAL - audit trail)
- documents
- payments
- permits
- alerts
- audit_logs
```

## Collection Schemas

### users
```javascript
{
  _id: ObjectId,
  username: String,           // "admin_01", "port_officer_01"
  email: String,
  role: String,               // "admin", "port_officer", "checkpoint_officer", "driver"
  full_name: String,
  organization_id: ObjectId,  // Reference to organizations
  is_active: Boolean,
  created_at: ISODate,
  updated_at: ISODate
}

Indexes:
- { username: 1 } (unique)
- { role: 1 }
- { organization_id: 1 }
```

### organizations
```javascript
{
  _id: ObjectId,
  name: String,               // "Gwadar Port Authority"
  registration_number: String,
  contact_email: String,
  contact_phone: String,
  address: String,
  type: String,               // "port", "logistics", "checkpoint"
  created_at: ISODate
}
```

### drivers
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,          // Reference to users
  license_number: String,
  license_expiry: ISODate,
  phone: String,
  status: String,             // "active", "inactive"
  created_at: ISODate
}

Indexes:
- { user_id: 1 } (unique)
- { license_number: 1 } (unique)
```

### vehicles
```javascript
{
  _id: ObjectId,
  registration_number: String, // "BLA-2045"
  vehicle_type: String,        // "truck", "container_truck"
  capacity_tons: Number,
  owner_id: ObjectId,          // Reference to organizations
  driver_id: ObjectId,         // Reference to drivers
  status: String,              // "available", "in_transit", "maintenance"
  created_at: ISODate,
  updated_at: ISODate
}

Indexes:
- { registration_number: 1 } (unique)
- { driver_id: 1 }
- { status: 1 }
```

### containers
```javascript
{
  _id: ObjectId,
  container_number: String,   // "MSKU-XXXXXX"
  type: String,               // "20ft", "40ft"
  capacity_tons: Number,
  owner_id: ObjectId,         // Reference to organizations
  current_location: String,
  status: String,             // "at_port", "in_transit", "delivered"
  created_at: ISODate
}

Indexes:
- { container_number: 1 } (unique)
```

### cargo
```javascript
{
  _id: ObjectId,
  cargo_id: String,           // "GWD-2026-001284" (unique identifier)
  container_id: ObjectId,     // Reference to containers
  category: String,           // "electronics", "textiles", "food"
  description: String,
  weight_tons: Number,
  quantity: Number,
  origin: String,             // "Gwadar Port"
  destination: String,        // "Quetta"
  importer_id: ObjectId,      // Reference to organizations
  exporter_id: ObjectId,      // Reference to organizations
  consignee: String,
  status: String,             // "registered", "verified", "in_transit", "delivered"
  created_at: ISODate,
  updated_at: ISODate
}

Indexes:
- { cargo_id: 1 } (unique)
- { status: 1 }
- { destination: 1 }
```

### shipments
```javascript
{
  _id: ObjectId,
  shipment_id: String,        // "GWD-2026-001284" (same as cargo_id)
  cargo_id: ObjectId,         // Reference to cargo
  vehicle_id: ObjectId,       // Reference to vehicles
  driver_id: ObjectId,        // Reference to drivers
  route_id: ObjectId,         // Reference to routes
  seal_number: String,        // Container seal
  customs_status: String,     // "cleared", "pending"
  permit_status: String,      // "valid", "expired", "pending"
  payment_status: String,     // "paid", "pending", "overdue"
  tax_status: String,         // "paid", "pending"
  authorized_route: [String],  // ["Gwadar", "CP-01", "CP-02", "CP-03", "Quetta"]
  current_checkpoint: String, // "CP-02"
  next_checkpoint: String,    // "CP-03"
  expected_departure: ISODate,
  expected_arrival: ISODate,
  actual_departure: ISODate,
  actual_arrival: ISODate,
  status: String,             // "registered", "at_port", "in_transit", "flagged", "completed"
  qr_token: String,           // Signed verification token
  created_at: ISODate,
  updated_at: ISODate
}

Indexes:
- { shipment_id: 1 } (unique)
- { cargo_id: 1 } (unique)
- { vehicle_id: 1 }
- { status: 1 }
- { current_checkpoint: 1 }
```

### routes
```javascript
{
  _id: ObjectId,
  route_name: String,         // "Gwadar to Quetta"
  origin: String,             // "Gwadar Port"
  destination: String,        // "Quetta"
  checkpoints: [ObjectId],     // Array of checkpoint references
  distance_km: Number,
  estimated_duration_hours: Number,
  is_active: Boolean,
  created_at: ISODate
}

Indexes:
- { origin: 1, destination: 1 }
```

### checkpoints
```javascript
{
  _id: ObjectId,
  checkpoint_id: String,       // "CP-01", "CP-02"
  name: String,               // "Turbat Checkpoint"
  location: String,           // "Coastal Highway"
  coordinates: {
    lat: Number,
    lng: Number
  },
  type: String,               // "port_gate", "highway", "destination"
  officer_ids: [ObjectId],    // Assigned officers
  is_active: Boolean,
  created_at: ISODate
}

Indexes:
- { checkpoint_id: 1 } (unique)
- { type: 1 }
```

### journey_events (CRITICAL - Audit Trail)
```javascript
{
  _id: ObjectId,
  event_id: String,           // Unique event identifier
  shipment_id: ObjectId,      // Reference to shipments
  cargo_id: ObjectId,         // Reference to cargo
  checkpoint_id: ObjectId,    // Reference to checkpoints
  event_type: String,         // "cargo_registered", "document_verified", "truck_assigned", 
                              // "port_gate_exit", "checkpoint_scan", "destination_arrival",
                              // "seal_verified", "payment_verified", "alert_created"
  timestamp: ISODate,
  officer_id: ObjectId,       // Reference to users
  vehicle_id: ObjectId,       // Reference to vehicles
  seal_status: String,        // "verified", "mismatch", "not_checked"
  verification_status: String, // "success", "failed", "pending"
  remarks: String,
  metadata: {
    // Flexible field for additional event-specific data
    scanned_vehicle: String,
    expected_vehicle: String,
    scanned_seal: String,
    expected_seal: String,
    qr_token: String
  }
}

Indexes:
- { shipment_id: 1, timestamp: -1 }  // For journey timeline
- { checkpoint_id: 1, timestamp: -1 } // For checkpoint history
- { event_type: 1, timestamp: -1 }
- { timestamp: -1 } // For recent events query

IMPORTANT: Journey events are NEVER overwritten. 
Each interaction creates a new event record for complete audit trail.
```

### documents
```javascript
{
  _id: ObjectId,
  document_id: String,
  shipment_id: ObjectId,      // Reference to shipments
  document_type: String,      // "customs_clearance", "permit", "invoice", "insurance"
  document_number: String,
  issue_date: ISODate,
  expiry_date: ISODate,
  file_url: String,           // S3 or local file path
  status: String,             // "valid", "expired", "pending"
  created_at: ISODate
}

Indexes:
- { shipment_id: 1 }
- { document_type: 1 }
```

### payments
```javascript
{
  _id: ObjectId,
  payment_id: String,
  shipment_id: ObjectId,      // Reference to shipments
  amount: Number,
  currency: String,           // "PKR"
  payment_type: String,        // "tax", "toll", "fee"
  status: String,             // "paid", "pending", "overdue"
  payment_date: ISODate,
  due_date: ISODate,
  created_at: ISODate
}

Indexes:
- { shipment_id: 1 }
- { status: 1 }
```

### permits
```javascript
{
  _id: ObjectId,
  permit_id: String,
  shipment_id: ObjectId,      // Reference to shipments
  permit_type: String,        // "transport", "hazardous", "special"
  issue_date: ISODate,
  expiry_date: ISODate,
  issuing_authority: String,
  status: String,             // "valid", "expired", "revoked"
  created_at: ISODate
}

Indexes:
- { shipment_id: 1 }
- { permit_id: 1 } (unique)
```

### alerts
```javascript
{
  _id: ObjectId,
  alert_id: String,
  shipment_id: ObjectId,      // Reference to shipments
  alert_type: String,         // "vehicle_mismatch", "checkpoint_sequence", "seal_mismatch",
                              // "permit_expired", "payment_pending", "route_deviation",
                              // "duplicate_qr", "cargo_mismatch"
  severity: String,           // "critical", "warning", "info"
  message: String,
  checkpoint_id: ObjectId,    // Where alert was triggered
  is_resolved: Boolean,
  resolved_by: ObjectId,      // Reference to users
  resolved_at: ISODate,
  created_at: ISODate
}

Indexes:
- { shipment_id: 1, is_resolved: 1 }
- { severity: 1, is_resolved: 1 }
- { created_at: -1 }
```

### audit_logs
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,          // Reference to users
  action: String,             // "create", "update", "delete", "scan"
  resource_type: String,     // "shipment", "cargo", "vehicle"
  resource_id: ObjectId,
  changes: {
    before: Object,          // Previous state
    after: Object            // New state
  },
  ip_address: String,
  timestamp: ISODate
}

Indexes:
- { user_id: 1, timestamp: -1 }
- { resource_type: 1, resource_id: 1 }
- { timestamp: -1 }
```

## Relationship Diagram

```
organizations (1) ──< (N) users
organizations (1) ──< (N) vehicles
organizations (1) ──< (N) containers

users (1) ──< (1) drivers
drivers (1) ──< (N) vehicles

cargo (1) ──< (1) shipments
shipments (1) ──< (1) vehicles
shipments (1) ──< (1) drivers
shipments (1) ──< (1) routes
shipments (1) ──< (N) journey_events
shipments (1) ──< (N) documents
shipments (1) ──< (N) payments
shipments (1) ──< (N) permits
shipments (1) ──< (N) alerts

routes (1) ──< (N) checkpoints
checkpoints (1) ──< (N) users (officers)
checkpoints (1) ──< (N) journey_events
```

## Sample Data Structure

### Sample Shipment with Journey Events
```javascript
// Shipment
{
  _id: ObjectId("..."),
  shipment_id: "GWD-2026-001284",
  cargo_id: ObjectId("..."),
  vehicle_id: ObjectId("..."),
  driver_id: ObjectId("..."),
  route_id: ObjectId("..."),
  seal_number: "SEAL-12345",
  customs_status: "cleared",
  permit_status: "valid",
  payment_status: "paid",
  tax_status: "paid",
  authorized_route: ["Gwadar", "CP-01", "CP-02", "CP-03", "Quetta"],
  current_checkpoint: "CP-02",
  next_checkpoint: "CP-03",
  status: "in_transit"
}

// Journey Events (Chronological)
[
  {
    event_type: "cargo_registered",
    timestamp: ISODate("2026-09-27T09:12:00Z"),
    verification_status: "success"
  },
  {
    event_type: "document_verified",
    timestamp: ISODate("2026-09-27T09:26:00Z"),
    verification_status: "success"
  },
  {
    event_type: "truck_assigned",
    timestamp: ISODate("2026-09-27T09:31:00Z"),
    verification_status: "success"
  },
  {
    event_type: "port_gate_exit",
    timestamp: ISODate("2026-09-27T10:02:00Z"),
    verification_status: "success"
  },
  {
    event_type: "checkpoint_scan",
    timestamp: ISODate("2026-09-27T11:17:00Z"),
    checkpoint_id: ObjectId("CP-01"),
    verification_status: "success"
  },
  {
    event_type: "checkpoint_scan",
    timestamp: ISODate("2026-09-27T13:42:00Z"),
    checkpoint_id: ObjectId("CP-02"),
    verification_status: "success"
  }
]
```
