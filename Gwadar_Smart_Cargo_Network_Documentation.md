# Gwadar Smart Cargo Network

## Product & UI Documentation

### 1. Core Concept

A digital logistics and cargo-verification platform for cargo moving
from **Gwadar Port to inland destinations**.

Each shipment receives a **unique Cargo ID + secure QR code**. Every
authorized interaction---port entry/exit, driver assignment, checkpoint
scan, payment verification, seal verification, and final delivery---is
recorded against that Cargo ID.

**Core flow:**

`Cargo Registered → Documents Verified → Truck Assigned → QR Issued → Port Gate Scan → Checkpoints → Destination Verification → Journey Closed`

No AI is required. Detection is based on **predefined rules and
verification logic**.

------------------------------------------------------------------------

## 2. User Roles

The platform has **four primary roles**:

  -----------------------------------------------------------------------
  Role                                Purpose
  ----------------------------------- -----------------------------------
  **Admin / Control Room**            Monitor the entire Gwadar logistics
                                      network

  **Port / Gate Officer**             Register and release cargo from the
                                      port

  **Checkpoint Officer**              Verify trucks and cargo while
                                      travelling

  **Driver**                          Carry digital shipment credentials
                                      and see journey requirements
  -----------------------------------------------------------------------

All interfaces can use the **same backend/database** with role-based
access and dashboards.

------------------------------------------------------------------------

## 3. Admin / Control Room Portal

This should be the **hero interface** during the presentation.

### Dashboard

Top metric cards:

-   `1,284 Active Shipments`
-   `342 In Transit`
-   `86 Completed Today`
-   `12 Flagged`
-   `PKR ___ Charges Collected`

### Live Cargo Map

Show Gwadar Port and simulated cargo routes.

Suggested marker states:

-   🟢 Verified / Normal
-   🟡 Waiting at checkpoint
-   🔴 Flagged
-   ⚫ Journey completed

Clicking a truck displays:

-   Cargo ID
-   Container number
-   Vehicle registration
-   Origin and destination
-   Driver
-   Current checkpoint/location
-   Journey status
-   Seal status
-   Next checkpoint

Example:

> **GWD-CT-10284**\
> Container: MSKU-XXXX\
> Vehicle: BLA-2045\
> Gwadar → Quetta\
> Driver: Ahmed Khan\
> Current checkpoint: Turbat\
> Status: In Transit\
> Seal: Verified\
> Next checkpoint: CP-03

### Recent Movement

  Cargo       Truck      Location        Time    Status
  ----------- ---------- --------------- ------- ----------
  GWD-10284   BLA-2045   Port Gate       09:42   Verified
  GWD-10291   TKA-881    Checkpoint 02   10:01   Verified
  GWD-10301   QTA-921    Checkpoint 01   10:07   Flagged

### Alerts Center

Rule-based alerts can include:

-   Route deviation
-   Checkpoint skipped
-   QR already used
-   Seal mismatch
-   Permit expired
-   Tax/payment pending
-   Vehicle mismatch
-   Cargo mismatch

Admins can open an alert, inspect the complete shipment history, and
resolve or escalate it.

------------------------------------------------------------------------

## 4. Cargo Management

Admin or port officer selects:

### `+ Register Cargo`

#### Shipment

-   Cargo ID --- automatically generated
-   Container number
-   Cargo category
-   Cargo description
-   Weight
-   Quantity
-   Origin
-   Destination

#### Importer / Exporter

-   Company
-   Registration/reference number
-   Contact
-   Consignee

#### Vehicle

-   Truck registration
-   Vehicle type
-   Driver
-   Driver identification/reference

#### Compliance

-   Customs clearance/reference
-   Permit status
-   Tax status
-   Toll/payment status
-   Container seal number

#### Journey

-   Origin
-   Destination
-   Authorized route
-   Required checkpoints
-   Expected departure
-   Expected arrival

Relevant documents can also be attached.

### Generate Cargo Pass

The system generates a unique Cargo ID, for example:

`GWD-2026-001284`

along with a secure QR code.

------------------------------------------------------------------------

## 5. QR Cargo Passport

When the QR is scanned, sensitive cargo information should **not** be
stored directly inside the QR.

An authorized officer sees:

> **DIGITAL CARGO PASS**
>
> Cargo ID: GWD-2026-001284\
> Container: MSKU-XXXXXX\
> Truck: BLA-2045\
> Route: Gwadar → Quetta\
> Driver: Ahmed Khan
>
> Customs: ✓\
> Permit: ✓\
> Payment: ✓\
> Seal: ✓
>
> Previous checkpoint: Gwadar Gate\
> Next checkpoint: CP-02
>
> **AUTHORIZED**

### QR Architecture

The QR should contain something similar to:

`Cargo ID + signed verification token`

The server then retrieves the actual cargo record.

This prevents sensitive shipment data from being directly embedded in
the QR code.

------------------------------------------------------------------------

## 6. Port / Gate Officer Portal

The interface should prioritize speed and simplicity.

### Home Screen

A large:

`[ Scan QR ]`

button.

### Shipment Verification

After scanning:

> GWD-2026-001284\
> BLA-2045\
> Gwadar → Quetta

Four large verification indicators:

-   **Cargo ✓**
-   **Vehicle ✓**
-   **Documents ✓**
-   **Payments ✓**

If all required conditions are satisfied:

### 🟢 CLEARED FOR EXIT

Officer selects:

`Confirm Departure`

The system records:

-   Gwadar Port Gate
-   Date
-   Time
-   Officer ID
-   Vehicle
-   Status: Departed

------------------------------------------------------------------------

## 7. Checkpoint Officer Portal

The checkpoint interface should be extremely fast.

### Checkpoint Home

> **Checkpoint CP-03**\
> Coastal Highway

Main action:

`[ SCAN QR ]`

### Successful Verification

## ✓ VERIFIED

Display:

-   Cargo ID
-   Vehicle
-   Route status
-   Seal status
-   Previous checkpoint
-   Current checkpoint

Primary action:

`ALLOW`

### Verification Failure

## ⚠ VERIFICATION REQUIRED

Example:

> **Vehicle mismatch**
>
> Expected: BLA-2045\
> Scanned/entered: BLA-9082

Available actions:

-   `Hold Shipment`
-   `Report Issue`
-   `Contact Control Room`

------------------------------------------------------------------------

## 8. Driver Interface

The driver interface should be **mobile-first and minimal**.

### Driver Home

Example:

> Good afternoon, Ahmed
>
> **ACTIVE JOURNEY**
>
> Gwadar\
> ↓\
> CP-01 ✓\
> ↓\
> CP-02 ✓\
> ↓\
> CP-03\
> ↓\
> Quetta

Shipment information:

-   Cargo: GWD-001284
-   Truck: BLA-2045
-   ETA: 18:30

Main actions:

-   `Show Cargo QR`
-   `View Route`
-   `Documents`
-   `Report Problem`

### Driver Permissions

Drivers should **not** be able to edit:

-   Cargo information
-   Taxes
-   Permits
-   Checkpoints
-   Vehicle assignment
-   Verification records

Drivers can only view relevant information and present their digital
cargo pass.

------------------------------------------------------------------------

## 9. Journey Timeline

Each shipment has a complete chronological history.

### Example: GWD-001284

**Gwadar Port**

✓ Cargo Registered --- 09:12

↓

✓ Documents Verified --- 09:26

↓

✓ Truck Assigned --- 09:31

↓

✓ Port Gate Exit --- 10:02

↓

✓ Checkpoint 01 --- 11:17

↓

✓ Checkpoint 02 --- 13:42

↓

○ Checkpoint 03 --- Pending

↓

○ Destination --- Pending

This creates an understandable **digital chain of custody**.

------------------------------------------------------------------------

## 10. Rule Engine

The system does not require AI.

Deterministic rules can handle verification:

``` text
IF scanned_vehicle != assigned_vehicle
→ FLAG VEHICLE_MISMATCH

IF checkpoint != expected_next_checkpoint
→ FLAG CHECKPOINT_SEQUENCE

IF permit_expiry < current_date
→ BLOCK SHIPMENT

IF payment_status != PAID
→ BLOCK PORT_EXIT

IF seal_number != registered_seal
→ FLAG SEAL_MISMATCH

IF QR_status == already_completed
→ FLAG DUPLICATE_USE
```

Every decision is therefore **deterministic, explainable, and
auditable**.

------------------------------------------------------------------------

## 11. Database Structure

Suggested collections/tables:

``` text
Users
Organizations
Drivers
Vehicles
Containers
Cargo
Shipments
Routes
Checkpoints
JourneyEvents
Documents
Payments
Permits
Alerts
AuditLogs
```

### JourneyEvents

One of the most important tables:

``` text
event_id
shipment_id
checkpoint_id
event_type
timestamp
officer_id
vehicle_id
seal_status
verification_status
remarks
```

Journey history should **never be overwritten**.

Each interaction creates a new event record, providing a permanent audit
trail.

------------------------------------------------------------------------

## 12. UI Design Direction

The platform should **not** look like a colorful generic startup
dashboard.

Design direction:

**Port Command Center + Modern Infrastructure System**

### Admin Desktop

-   Dark navy sidebar
-   White/light-gray workspace
-   Large live map
-   Compact data tables
-   Green verification states
-   Amber warnings
-   Red critical alerts
-   Minimal rounded corners
-   Strong typography
-   Information-dense but clean layout

### Checkpoint Mobile/Tablet UI

Checkpoint officers need speed rather than analytics:

-   Huge scanner button
-   Large verification status
-   Large action buttons
-   Minimal information
-   High readability

An officer standing beside a truck should not need to navigate through
charts or complex menus.

------------------------------------------------------------------------

## 13. Hackathon Demo Scenario

### Step 1 --- Register Cargo

Start with:

> **A container arrives at Gwadar Port.**

Register the shipment and generate its Cargo QR.

### Step 2 --- Port Clearance

Switch to the Port Officer interface.

Scan the QR.

Result:

**CLEARED**

### Step 3 --- Begin Journey

Switch to the Admin Control Room.

The truck appears on the dashboard as:

**IN TRANSIT**

### Step 4 --- Checkpoint Verification

Switch to the Checkpoint Officer interface.

Scan the QR.

Result:

**VERIFIED**

### Step 5 --- Simulate a Violation

Deliberately modify the truck number or seal information.

Scan the cargo at the next checkpoint.

Result:

### 🔴 VEHICLE / SEAL MISMATCH

The Admin dashboard immediately displays:

> **GWD-001284 --- Verification Required**

Open the shipment to display its complete cargo journey and verification
history.

------------------------------------------------------------------------

## Core Pitch

> **"We aren't just digitizing a container. We're creating a verifiable
> digital journey from Gwadar Port to its destination."**

The core innovation is a **connected cargo identity, verification
network, and auditable chain of custody** across Gwadar's port-to-road
logistics journey.
