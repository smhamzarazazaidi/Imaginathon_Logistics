# UI/UX Design System

## Design Philosophy

**Port Command Center + Modern Infrastructure System**

The UI should convey authority, precision, and real-time monitoring capabilities. Think air traffic control meets logistics dashboard - information-dense but clean, with clear visual hierarchy and immediate status recognition.

## Color Palette

### Primary Colors
```css
/* Navy Sidebar - Authority & Stability */
--navy-primary: #0a1929
--navy-secondary: #112240
--navy-light: #233554

/* Workspace - Clean & Professional */
--bg-primary: #ffffff
--bg-secondary: #f5f7fa
--bg-tertiary: #e8eaf0

/* Accent - Port Command Blue */
--accent-primary: #0066cc
--accent-secondary: #0088ff
--accent-light: #e6f2ff
```

### Status Colors
```css
/* Success - Verified */
--success: #10b981
--success-light: #d1fae5
--success-dark: #059669

/* Warning - Pending/Attention */
--warning: #f59e0b
--warning-light: #fef3c7
--warning-dark: #d97706

/* Critical - Flagged/Alert */
--critical: #ef4444
--critical-light: #fee2e2
--critical-dark: #dc2626

/* Info - Neutral */
--info: #6366f1
--info-light: #e0e7ff
--info-dark: #4f46e5

/* Completed - Journey Done */
--completed: #374151
--completed-light: #d1d5db
```

### Text Colors
```css
--text-primary: #111827
--text-secondary: #4b5563
--text-tertiary: #9ca3af
--text-inverse: #ffffff
```

## Typography

### Font Family
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
--font-mono: 'JetBrains Mono', 'Fira Code', monospace
```

### Type Scale
```css
/* Display */
--text-4xl: 2.25rem;    /* 36px - Page titles */
--text-3xl: 1.875rem;   /* 30px - Section headers */
--text-2xl: 1.5rem;     /* 24px - Card titles */

/* Body */
--text-xl: 1.25rem;     /* 20px - Large text */
--text-lg: 1.125rem;    /* 18px - Body text */
--text-base: 1rem;      /* 16px - Default */
--text-sm: 0.875rem;    /* 14px - Small text */
--text-xs: 0.75rem;     /* 12px - Labels */

/* Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Typography Usage
- **Headings**: Semibold, tight letter-spacing (-0.02em)
- **Body**: Regular, comfortable line-height (1.6)
- **Data/Mono**: Monospace for IDs, timestamps, codes
- **Labels**: Uppercase, small, letter-spacing (0.1em)

## Spacing System

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

## Border Radius

```css
--radius-sm: 4px;      /* Small elements */
--radius-md: 6px;      /* Cards, buttons */
--radius-lg: 8px;      /* Large cards */
--radius-xl: 12px;     /* Modals */
--radius-full: 9999px; /* Pills, badges */
```

**Design Note**: Keep corners minimal. This is a professional infrastructure system, not a playful startup.

## Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
```

## Component Specifications

### Buttons

#### Primary Button
```css
background: var(--accent-primary);
color: white;
padding: var(--space-3) var(--space-6);
border-radius: var(--radius-md);
font-weight: var(--font-semibold);
transition: all 0.2s ease;

&:hover {
  background: var(--accent-secondary);
  transform: translateY(-1px);
}
```

#### Secondary Button
```css
background: white;
color: var(--accent-primary);
border: 1px solid var(--accent-primary);
padding: var(--space-3) var(--space-6);
border-radius: var(--radius-md);
font-weight: var(--font-semibold);
```

#### Critical Button
```css
background: var(--critical);
color: white;
padding: var(--space-3) var(--space-6);
border-radius: var(--radius-md);
font-weight: var(--font-semibold);
```

#### Large Scanner Button (Checkpoint)
```css
background: var(--success);
color: white;
padding: var(--space-8) var(--space-12);
border-radius: var(--radius-lg);
font-size: var(--text-xl);
font-weight: var(--font-bold);
min-width: 200px;
min-height: 200px;
box-shadow: var(--shadow-lg);
```

### Cards

#### Metric Card
```css
background: white;
border-radius: var(--radius-lg);
padding: var(--space-6);
border: 1px solid var(--bg-tertiary);
box-shadow: var(--shadow-sm);

.metric-value {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
}

.metric-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

#### Shipment Card
```css
background: white;
border-radius: var(--radius-lg);
padding: var(--space-5);
border-left: 4px solid var(--success);
box-shadow: var(--shadow-md);
transition: all 0.2s ease;

&:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
}
```

### Status Indicators

#### Verified/Normal
```css
background: var(--success);
color: white;
padding: var(--space-1) var(--space-3);
border-radius: var(--radius-full);
font-size: var(--text-xs);
font-weight: var(--font-semibold);
```

#### Waiting/Pending
```css
background: var(--warning);
color: white;
padding: var(--space-1) var(--space-3);
border-radius: var(--radius-full);
font-size: var(--text-xs);
font-weight: var(--font-semibold);
```

#### Flagged/Critical
```css
background: var(--critical);
color: white;
padding: var(--space-1) var(--space-3);
border-radius: var(--radius-full);
font-size: var(--text-xs);
font-weight: var(--font-semibold);
animation: pulse 2s infinite;
```

### Tables

#### Data Table
```css
background: white;
border-radius: var(--radius-lg);
overflow: hidden;
border: 1px solid var(--bg-tertiary);

thead {
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--bg-tertiary);
}

th {
  padding: var(--space-4) var(--space-5);
  text-align: left;
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-secondary);
}

td {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--bg-tertiary);
  font-size: var(--text-sm);
  color: var(--text-primary);
}

tr:hover {
  background: var(--bg-secondary);
}
```

### Form Elements

#### Input Fields
```css
background: white;
border: 1px solid var(--bg-tertiary);
border-radius: var(--radius-md);
padding: var(--space-3) var(--space-4);
font-size: var(--text-base);
transition: border-color 0.2s ease;

&:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-light);
}
```

#### Select Dropdown
```css
background: white;
border: 1px solid var(--bg-tertiary);
border-radius: var(--radius-md);
padding: var(--space-3) var(--space-4);
font-size: var(--text-base);
appearance: none;
background-image: url("data:image/svg+xml...");
background-repeat: no-repeat;
background-position: right var(--space-3) center;
```

## Layout Patterns

### Admin Desktop Layout

```
┌─────────────────────────────────────────────────────────┐
│  Sidebar (Navy)  │  Main Workspace (White/Light Gray)   │
│                  │                                       │
│  ┌────────────┐  │  ┌───────────────────────────────┐  │
│  │ Logo       │  │  │  Header (Search, User, Alerts) │  │
│  ├────────────┤  │  ├───────────────────────────────┤  │
│  │ Dashboard  │  │  │                               │  │
│  │ Cargo      │  │  │  Metric Cards (4-5 across)   │  │
│  │ Vehicles   │  │  │                               │  │
│  │ Drivers    │  │  ├───────────────────────────────┤  │
│  │ Alerts     │  │  │                               │  │
│  │ Reports    │  │  │  Live Map (Large)              │  │
│  │ Settings   │  │  │                               │  │
│  └────────────┘  │  ├───────────────────────────────┤  │
│                  │  │                               │  │
│                  │  │  Recent Movements Table       │  │
│                  │  │  Alerts Center                │  │
│                  │  │                               │  │
│                  │  └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Checkpoint Mobile/Tablet Layout

```
┌─────────────────────────────────┐
│  CP-03 - Coastal Highway       │
│  Checkpoint Officer            │
├─────────────────────────────────┤
│                                 │
│         [ SCAN QR ]             │
│      (Large Button)             │
│                                 │
├─────────────────────────────────┤
│  Last Scan:                     │
│  GWD-10284                      │
│  ✓ VERIFIED                     │
│  10:42 AM                       │
└─────────────────────────────────┘
```

### Driver Mobile Layout

```
┌─────────────────────────────────┐
│  Good afternoon, Ahmed          │
├─────────────────────────────────┤
│  ACTIVE JOURNEY                 │
│                                 │
│  Gwadar                         │
│    ↓                            │
│  CP-01 ✓                        │
│    ↓                            │
│  CP-02 ✓                        │
│    ↓                            │
│  CP-03                          │
│    ↓                            │
│  Quetta                         │
├─────────────────────────────────┤
│  Cargo: GWD-001284              │
│  Truck: BLA-2045                │
│  ETA: 18:30                     │
├─────────────────────────────────┤
│  [Show QR] [Route] [Docs]       │
└─────────────────────────────────┘
```

## Responsive Design Rules

### Breakpoints
```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large Desktop */
```

### Mobile-First Strategy
1. **Default styles**: Mobile layout (single column)
2. **@media (min-width: md)**: Tablet (2 columns)
3. **@media (min-width: lg)**: Desktop (full layout)

### Critical Mobile Considerations
- Touch targets: minimum 44x44px
- Scanner button: minimum 200x200px
- Text size: minimum 16px to prevent zoom
- No hover states (use active states)
- Bottom navigation for driver app

## Animation & Transitions

### Micro-interactions
```css
/* Button hover */
transition: all 0.2s ease;

/* Card hover */
transition: all 0.3s ease;

/* Status change */
transition: background-color 0.5s ease;

/* Alert pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### Loading States
```css
/* Skeleton loader */
background: linear-gradient(
  90deg,
  var(--bg-tertiary) 25%,
  var(--bg-secondary) 50%,
  var(--bg-tertiary) 75%
);
background-size: 200% 100%;
animation: skeleton-loading 1.5s infinite;
```

### Real-time Updates
```css
/* New item highlight */
@keyframes highlight {
  0% { background: var(--accent-light); }
  100% { background: transparent; }
}

/* Status change flash */
@keyframes flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
```

## Accessibility

### Color Contrast
- All text: minimum 4.5:1 contrast ratio
- Large text: minimum 3:1 contrast ratio
- Interactive elements: minimum 3:1 contrast ratio

### Focus States
```css
*:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

### Screen Reader Support
- Semantic HTML elements
- ARIA labels for interactive elements
- Alt text for images
- Live regions for real-time updates

## Icon System

### Icon Library
Use Lucide Icons or Heroicons (lightweight, consistent)

### Icon Usage
```css
/* Size variants */
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }

/* Color variants */
.icon-primary { color: var(--accent-primary); }
.icon-success { color: var(--success); }
.icon-warning { color: var(--warning); }
.icon-critical { color: var(--critical); }
```

## Data Visualization

### Map Markers
- 🟢 Verified: Green circle with white border
- 🟡 Waiting: Yellow circle with white border
- 🔴 Flagged: Red circle with pulse animation
- ⚫ Completed: Gray circle

### Progress Indicators
```css
/* Journey progress bar */
background: var(--bg-tertiary);
border-radius: var(--radius-full);
height: 8px;

.progress-fill {
  background: var(--success);
  border-radius: var(--radius-full);
  height: 100%;
  transition: width 0.5s ease;
}
```

### Status Badges
```css
/* Compact status indicators */
display: inline-flex;
align-items: center;
gap: var(--space-2);
padding: var(--space-1) var(--space-2);
border-radius: var(--radius-full);
font-size: var(--text-xs);
font-weight: var(--font-semibold);
```

## Dark Mode (Optional)

For future consideration, maintain consistent contrast ratios and use:
```css
--bg-primary: #0a1929
--bg-secondary: #112240
--text-primary: #e8eaf0
--text-secondary: #9ca3af
```
