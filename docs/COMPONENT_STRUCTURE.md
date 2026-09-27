# Component Structure

## Frontend File Organization

```
frontend/
├── index.html                 # Entry point
├── css/
│   ├── main.css              # Global styles
│   ├── components.css        # Component styles
│   ├── admin.css             # Admin-specific styles
│   ├── port.css              # Port officer styles
│   ├── checkpoint.css        # Checkpoint styles
│   └── driver.css            # Driver mobile styles
├── js/
│   ├── main.js              # App initialization
│   ├── api.js               # API client
│   ├── websocket.js         # WebSocket client
│   ├── utils.js             # Utility functions
│   ├── components/
│   │   ├── navbar.js        # Navigation component
│   │   ├── sidebar.js       # Sidebar component
│   │   ├── metric-card.js   # Metric card component
│   │   ├── shipment-card.js # Shipment card component
│   │   ├── alert-card.js    # Alert card component
│   │   ├── status-badge.js  # Status badge component
│   │   ├── qr-scanner.js    # QR scanner component
│   │   └── journey-timeline.js # Timeline component
│   ├── pages/
│   │   ├── admin/
│   │   │   ├── dashboard.js
│   │   │   ├── cargo-management.js
│   │   │   ├── live-map.js
│   │   │   └── alerts.js
│   │   ├── port/
│   │   │   ├── dashboard.js
│   │   │   └── verification.js
│   │   ├── checkpoint/
│   │   │   └── scanner.js
│   │   └── driver/
│   │       └── mobile-app.js
│   └── state/
│       ├── store.js         # Global state management
│       └── reducers.js      # State reducers
└── assets/
    ├── images/
    └── icons/
```

## Reusable Component List

### Navigation Components

#### Navbar
```javascript
// components/navbar.js
class Navbar {
  constructor(user) {
    this.user = user;
  }

  render() {
    return `
      <nav class="navbar">
        <div class="navbar-brand">Gwadar Cargo Network</div>
        <div class="navbar-user">
          <span class="user-name">${this.user.full_name}</span>
          <span class="user-role">${this.user.role}</span>
          <button class="logout-btn">Logout</button>
        </div>
      </nav>
    `;
  }
}
```

#### Sidebar
```javascript
// components/sidebar.js
class Sidebar {
  constructor(currentPage, userRole) {
    this.currentPage = currentPage;
    this.userRole = userRole;
  }

  render() {
    const menuItems = this.getMenuForRole(this.userRole);
    return `
      <aside class="sidebar">
        <div class="sidebar-menu">
          ${menuItems.map(item => `
            <a href="${item.href}" class="sidebar-item ${item.href === this.currentPage ? 'active' : ''}">
              <span class="sidebar-icon">${item.icon}</span>
              <span class="sidebar-label">${item.label}</span>
            </a>
          `).join('')}
        </div>
      </aside>
    `;
  }

  getMenuForRole(role) {
    const menus = {
      admin: [
        { href: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
        { href: '/admin/cargo', label: 'Cargo Management', icon: '📦' },
        { href: '/admin/vehicles', label: 'Vehicles', icon: '🚛' },
        { href: '/admin/drivers', label: 'Drivers', icon: '👤' },
        { href: '/admin/alerts', label: 'Alerts', icon: '🚨' },
        { href: '/admin/reports', label: 'Reports', icon: '📈' },
      ],
      port_officer: [
        { href: '/port/dashboard', label: 'Dashboard', icon: '📊' },
        { href: '/port/verification', label: 'Verification', icon: '✓' },
      ],
      checkpoint_officer: [
        { href: '/checkpoint/scanner', label: 'Scanner', icon: '📷' },
      ],
      driver: [
        { href: '/driver/dashboard', label: 'My Journey', icon: '📍' },
      ]
    };
    return menus[role] || [];
  }
}
```

### Data Display Components

#### Metric Card
```javascript
// components/metric-card.js
class MetricCard {
  constructor({ label, value, trend, icon }) {
    this.label = label;
    this.value = value;
    this.trend = trend;
    this.icon = icon;
  }

  render() {
    return `
      <div class="metric-card">
        <div class="metric-header">
          <span class="metric-icon">${this.icon}</span>
          <span class="metric-label">${this.label}</span>
        </div>
        <div class="metric-value">${this.value}</div>
        ${this.trend ? `<div class="metric-trend ${this.trend.direction}">${this.trend.value}</div>` : ''}
      </div>
    `;
  }
}
```

#### Shipment Card
```javascript
// components/shipment-card.js
class ShipmentCard {
  constructor(shipment) {
    this.shipment = shipment;
  }

  render() {
    const statusColor = this.getStatusColor(this.shipment.status);
    return `
      <div class="shipment-card" data-shipment-id="${this.shipment.shipment_id}">
        <div class="shipment-header">
          <div class="shipment-id">${this.shipment.shipment_id}</div>
          <div class="shipment-status ${statusColor}">${this.shipment.status}</div>
        </div>
        <div class="shipment-details">
          <div class="detail-row">
            <span class="detail-label">Container:</span>
            <span class="detail-value">${this.shipment.container_number}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Vehicle:</span>
            <span class="detail-value">${this.shipment.vehicle_registration}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Route:</span>
            <span class="detail-value">${this.shipment.origin} → ${this.shipment.destination}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Driver:</span>
            <span class="detail-value">${this.shipment.driver_name}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Current:</span>
            <span class="detail-value">${this.shipment.current_checkpoint}</span>
          </div>
        </div>
        <div class="shipment-actions">
          <button class="btn-view-details">View Details</button>
        </div>
      </div>
    `;
  }

  getStatusColor(status) {
    const colors = {
      'in_transit': 'green',
      'flagged': 'red',
      'completed': 'gray',
      'at_port': 'blue',
      'registered': 'yellow'
    };
    return colors[status] || 'gray';
  }
}
```

#### Alert Card
```javascript
// components/alert-card.js
class AlertCard {
  constructor(alert) {
    this.alert = alert;
  }

  render() {
    const severityClass = this.getSeverityClass(this.alert.severity);
    return `
      <div class="alert-card ${severityClass}">
        <div class="alert-header">
          <span class="alert-icon">${this.getAlertIcon(this.alert.alert_type)}</span>
          <span class="alert-type">${this.alert.alert_type}</span>
          <span class="alert-severity">${this.alert.severity}</span>
        </div>
        <div class="alert-message">${this.alert.message}</div>
        <div class="alert-shipment">Shipment: ${this.alert.shipment_id}</div>
        <div class="alert-actions">
          <button class="btn-resolve">Resolve</button>
          <button class="btn-view">View Shipment</button>
        </div>
      </div>
    `;
  }

  getSeverityClass(severity) {
    return `alert-${severity}`;
  }

  getAlertIcon(type) {
    const icons = {
      'vehicle_mismatch': '🚛',
      'checkpoint_sequence': '📍',
      'seal_mismatch': '🔒',
      'permit_expired': '📄',
      'payment_pending': '💰',
      'route_deviation': '↗️',
      'duplicate_qr': '📱',
      'cargo_mismatch': '📦'
    };
    return icons[type] || '⚠️';
  }
}
```

#### Status Badge
```javascript
// components/status-badge.js
class StatusBadge {
  constructor(status) {
    this.status = status;
  }

  render() {
    const config = this.getStatusConfig(this.status);
    return `
      <span class="status-badge ${config.class}">
        <span class="status-dot"></span>
        ${config.label}
      </span>
    `;
  }

  getStatusConfig(status) {
    const configs = {
      'verified': { class: 'success', label: 'Verified' },
      'pending': { class: 'warning', label: 'Pending' },
      'flagged': { class: 'critical', label: 'Flagged' },
      'completed': { class: 'completed', label: 'Completed' },
      'in_transit': { class: 'info', label: 'In Transit' }
    };
    return configs[status] || { class: 'neutral', label: status };
  }
}
```

### Interactive Components

#### QR Scanner
```javascript
// components/qr-scanner.js
class QRScanner {
  constructor(onScan) {
    this.onScan = onScan;
    this.scanner = null;
  }

  async init() {
    // Initialize camera or file input for QR scanning
    this.scanner = new Html5Qrcode("qr-reader");
    await this.scanner.start(
      { facingMode: "environment" },
      { fps: 10, qrbox: { width: 250, height: 250 } },
      this.onScan,
      (errorMessage) => {
        // Handle scan errors
      }
    );
  }

  stop() {
    if (this.scanner) {
      this.scanner.stop();
    }
  }

  render() {
    return `
      <div class="qr-scanner">
        <div id="qr-reader"></div>
        <button class="btn-stop-scan">Stop Scanning</button>
      </div>
    `;
  }
}
```

#### Journey Timeline
```javascript
// components/journey-timeline.js
class JourneyTimeline {
  constructor(events) {
    this.events = events;
  }

  render() {
    return `
      <div class="journey-timeline">
        ${this.events.map((event, index) => `
          <div class="timeline-item ${event.verification_status}">
            <div class="timeline-marker">
              ${this.getMarkerIcon(event.event_type)}
            </div>
            <div class="timeline-content">
              <div class="timeline-event">${this.formatEventType(event.event_type)}</div>
              <div class="timeline-time">${this.formatTime(event.timestamp)}</div>
              <div class="timeline-location">${event.checkpoint_id || 'Gwadar Port'}</div>
              ${event.remarks ? `<div class="timeline-remarks">${event.remarks}</div>` : ''}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  getMarkerIcon(eventType) {
    const icons = {
      'cargo_registered': '📦',
      'document_verified': '📄',
      'truck_assigned': '🚛',
      'port_gate_exit': '🚪',
      'checkpoint_scan': '📍',
      'destination_arrival': '🏁'
    };
    return icons[eventType] || '✓';
  }

  formatEventType(type) {
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString();
  }
}
```

## Page-by-Page Component Breakdown

### Admin Dashboard

```javascript
// pages/admin/dashboard.js
class AdminDashboard {
  constructor() {
    this.metricCards = [];
    this.liveMap = null;
    this.recentMovements = [];
    this.alerts = [];
  }

  async init() {
    await this.loadMetrics();
    await this.loadLiveMap();
    await this.loadRecentMovements();
    await this.loadAlerts();
    this.setupWebSocket();
    this.render();
  }

  render() {
    return `
      <div class="admin-dashboard">
        <div class="metrics-grid">
          ${this.metricCards.map(card => card.render()).join('')}
        </div>
        <div class="dashboard-main">
          <div class="live-map-section">
            <h2>Live Cargo Map</h2>
            <div id="live-map"></div>
          </div>
          <div class="recent-movements-section">
            <h2>Recent Movements</h2>
            <table class="movements-table">
              <!-- Table content -->
            </table>
          </div>
        </div>
        <div class="alerts-section">
          <h2>Alerts Center</h2>
          <div class="alerts-grid">
            ${this.alerts.map(alert => new AlertCard(alert).render()).join('')}
          </div>
        </div>
      </div>
    `;
  }
}
```

### Port Officer Verification

```javascript
// pages/port/verification.js
class PortVerification {
  constructor() {
    this.qrScanner = new QRScanner(this.handleScan.bind(this));
    this.currentShipment = null;
  }

  async init() {
    this.render();
    this.qrScanner.init();
  }

  handleScan(qrToken) {
    // Verify QR token with backend
    this.verifyShipment(qrToken);
  }

  async verifyShipment(qrToken) {
    const response = await API.post('/api/qr/verify', { qr_token: qrToken });
    this.currentShipment = response.shipment;
    this.renderVerificationResult();
  }

  render() {
    return `
      <div class="port-verification">
        <div class="verification-header">
          <h1>Port Gate Verification</h1>
        </div>
        <div class="scanner-section">
          ${this.qrScanner.render()}
        </div>
        ${this.currentShipment ? this.renderVerificationResult() : ''}
      </div>
    `;
  }

  renderVerificationResult() {
    const verification = this.currentShipment.verification_details;
    return `
      <div class="verification-result">
        <div class="shipment-info">
          <h2>${this.currentShipment.shipment_id}</h2>
          <p>${this.currentShipment.vehicle_registration}</p>
          <p>${this.currentShipment.origin} → ${this.currentShipment.destination}</p>
        </div>
        <div class="verification-indicators">
          <div class="indicator ${verification.cargo ? 'success' : 'error'}">
            <span class="indicator-icon">${verification.cargo ? '✓' : '✗'}</span>
            <span class="indicator-label">Cargo</span>
          </div>
          <div class="indicator ${verification.vehicle ? 'success' : 'error'}">
            <span class="indicator-icon">${verification.vehicle ? '✓' : '✗'}</span>
            <span class="indicator-label">Vehicle</span>
          </div>
          <div class="indicator ${verification.documents ? 'success' : 'error'}">
            <span class="indicator-icon">${verification.documents ? '✓' : '✗'}</span>
            <span class="indicator-label">Documents</span>
          </div>
          <div class="indicator ${verification.payments ? 'success' : 'error'}">
            <span class="indicator-icon">${verification.payments ? '✓' : '✗'}</span>
            <span class="indicator-label">Payments</span>
          </div>
        </div>
        ${this.isAllVerified() ? `
          <div class="cleared-badge">
            🟢 CLEARED FOR EXIT
          </div>
          <button class="btn-confirm-departure">Confirm Departure</button>
        ` : ''}
      </div>
    `;
  }

  isAllVerified() {
    const v = this.currentShipment.verification_details;
    return v.cargo && v.vehicle && v.documents && v.payments;
  }
}
```

### Checkpoint Scanner

```javascript
// pages/checkpoint/scanner.js
class CheckpointScanner {
  constructor(checkpointId) {
    this.checkpointId = checkpointId;
    this.qrScanner = new QRScanner(this.handleScan.bind(this));
  }

  async init() {
    this.render();
    this.qrScanner.init();
  }

  handleScan(qrToken) {
    this.verifyAtCheckpoint(qrToken);
  }

  async verifyAtCheckpoint(qrToken) {
    const response = await API.post('/api/checkpoints/scan', {
      qr_token: qrToken,
      checkpoint_id: this.checkpointId,
      action: 'allow'
    });
    this.renderResult(response);
  }

  render() {
    return `
      <div class="checkpoint-scanner">
        <div class="checkpoint-header">
          <h1>Checkpoint ${this.checkpointId}</h1>
          <p>Coastal Highway</p>
        </div>
        <div class="scanner-section">
          ${this.qrScanner.render()}
        </div>
        <div id="scan-result"></div>
      </div>
    `;
  }

  renderResult(result) {
    const resultDiv = document.getElementById('scan-result');
    if (result.verification_status === 'success') {
      resultDiv.innerHTML = `
        <div class="scan-success">
          <h2>✓ VERIFIED</h2>
          <div class="shipment-details">
            <p>Cargo ID: ${result.shipment_id}</p>
            <p>Vehicle: ${result.vehicle_registration}</p>
            <p>Status: ${result.status}</p>
          </div>
          <button class="btn-allow">ALLOW</button>
        </div>
      `;
    } else {
      resultDiv.innerHTML = `
        <div class="scan-failure">
          <h2>⚠ VERIFICATION REQUIRED</h2>
          <p>${result.message}</p>
          <button class="btn-hold">Hold Shipment</button>
          <button class="btn-report">Report Issue</button>
          <button class="btn-contact">Contact Control Room</button>
        </div>
      `;
    }
  }
}
```

### Driver Mobile App

```javascript
// pages/driver/mobile-app.js
class DriverMobileApp {
  constructor(driverId) {
    this.driverId = driverId;
    this.activeJourney = null;
  }

  async init() {
    await this.loadActiveJourney();
    this.setupWebSocket();
    this.render();
  }

  async loadActiveJourney() {
    const response = await API.get(`/api/drivers/${this.driverId}/active-journey`);
    this.activeJourney = response.journey;
  }

  render() {
    if (!this.activeJourney) {
      return `
        <div class="driver-app">
          <div class="no-journey">
            <h1>No Active Journey</h1>
            <p>Contact dispatch for assignment</p>
          </div>
        </div>
      `;
    }

    return `
      <div class="driver-app">
        <div class="driver-header">
          <h1>Good afternoon, ${this.activeJourney.driver_name}</h1>
        </div>
        <div class="active-journey">
          <h2>ACTIVE JOURNEY</h2>
          <div class="journey-route">
            ${this.renderRoute()}
          </div>
          <div class="journey-info">
            <p>Cargo: ${this.activeJourney.cargo_id}</p>
            <p>Truck: ${this.activeJourney.vehicle_registration}</p>
            <p>ETA: ${this.activeJourney.eta}</p>
          </div>
          <div class="journey-actions">
            <button class="btn-show-qr">Show Cargo QR</button>
            <button class="btn-view-route">View Route</button>
            <button class="btn-documents">Documents</button>
            <button class="btn-report">Report Problem</button>
          </div>
        </div>
      </div>
    `;
  }

  renderRoute() {
    const checkpoints = this.activeJourney.authorized_route;
    const current = this.activeJourney.current_checkpoint;
    return checkpoints.map((cp, index) => {
      const isCompleted = checkpoints.indexOf(current) > index;
      const isCurrent = cp === current;
      return `
        <div class="route-point ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''}">
          <span class="point-name">${cp}</span>
          ${isCompleted ? '<span class="point-check">✓</span>' : ''}
          ${index < checkpoints.length - 1 ? '<div class="route-line"></div>' : ''}
        </div>
      `;
    }).join('');
  }
}
```

## State Management Strategy

### Simple Store Pattern

```javascript
// state/store.js
class Store {
  constructor() {
    this.state = {
      user: null,
      shipments: [],
      alerts: [],
      metrics: null,
      websocketConnected: false
    };
    this.listeners = [];
  }

  getState() {
    return this.state;
  }

  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.notifyListeners();
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notifyListeners() {
    this.listeners.forEach(listener => listener(this.state));
  }
}

const store = new Store();
```

### Usage Example

```javascript
// In component
store.subscribe((state) => {
  if (state.shipments !== this.shipments) {
    this.shipments = state.shipments;
    this.render();
  }
});

// Update state
store.setState({ shipments: newShipments });
```

## Event Handling Patterns

### API Client

```javascript
// js/api.js
class API {
  static async get(url) {
    const response = await fetch(url);
    return response.json();
  }

  static async post(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  static async put(url, data) {
    const response = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
}
```

### WebSocket Client

```javascript
// js/websocket.js
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectInterval = 5000;
    this.subscriptions = new Set();
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.resubscribe();
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting...');
      setTimeout(() => this.connect(), this.reconnectInterval);
    };
  }

  subscribe(resource, resourceId) {
    this.subscriptions.add({ resource, resourceId });
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        resource,
        resource_id: resourceId
      }));
    }
  }

  handleMessage(message) {
    // Dispatch to appropriate handlers
    const handlers = {
      'cargo_status_update': this.handleCargoUpdate,
      'alert_created': this.handleAlert,
      'dashboard_update': this.handleDashboardUpdate
    };
    
    const handler = handlers[message.type];
    if (handler) {
      handler.call(this, message.data);
    }
  }

  handleCargoUpdate(data) {
    store.setState({
      shipments: store.getState().shipments.map(s =>
        s.shipment_id === data.shipment_id ? { ...s, ...data } : s
      )
    });
  }
}
```

## Utility Functions

```javascript
// js/utils.js
const Utils = {
  formatDate(date) {
    return new Date(date).toLocaleDateString();
  },

  formatTime(date) {
    return new Date(date).toLocaleTimeString();
  },

  formatDateTime(date) {
    return new Date(date).toLocaleString();
  },

  formatCurrency(amount, currency = 'PKR') {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency
    }).format(amount);
  },

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  generateId() {
    return Math.random().toString(36).substr(2, 9);
  }
};
```
