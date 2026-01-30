# QR System Architecture - Visual Guide

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PG MANAGEMENT - QR ENHANCEMENT v2.0                  │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
                         AUTHENTICATED ADMIN FLOW
═══════════════════════════════════════════════════════════════════════════

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│              │         │              │         │              │
│  ADMIN HOME  │────────→│ CREATE ROOM  │────────→│   ROOM QR    │
│              │         │    FORM      │         │    PAGE      │
└──────────────┘         └──────────────┘         └──────────────┘
       ↑                         ↑                        │
       │                         │                   ┌────┴────┐
       │                  ┌──────┴──────┐            │         │
       │                  │             │            ↓         ↓
       └──────────────────┤ EDIT/DELETE ├─────── PRINT QR  COPY URL
                          │             │            │         │
                          └──────┬──────┘            │         │
                                 │                   │         │
                           ┌─────┴──────┐            │         │
                           │            │            │         │
                           ↓            ↓            └─────────┘
                      ┌─────────────────────┐
                      │  DATABASE UPDATED   │
                      │  ✓ Room Record      │
                      │  ✓ QR Generated     │
                      └─────────────────────┘


┌──────────────┐         ┌────────────────┐       ┌──────────────┐
│              │         │                │       │              │
│ROOM DETAILS  │────────→│ CREATE RESIDENT│──────→│ RESIDENT QR  │
│              │         │    FORM        │       │    PAGE      │
└──────────────┘         └────────────────┘       └──────────────┘
       ↑                         ↑                       │
       │                         │                  ┌────┴────┐
       │                  ┌──────┴──────┐           │         │
       │                  │             │           ↓         ↓
       └──────────────────┤ EDIT/DELETE ├──── PRINT QR  COPY URL
                          │             │           │         │
                          └──────┬──────┘           │         │
                                 │                  │         │
                           ┌─────┴──────┐           │         │
                           │            │           │         │
                           ↓            ↓           └─────────┘
                      ┌──────────────────────┐
                      │  DATABASE UPDATED    │
                      │  ✓ Resident Record   │
                      │  ✓ QR Generated      │
                      └──────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                        PUBLIC USER QR SCANNING FLOW
═══════════════════════════════════════════════════════════════════════════

┌──────────────────┐        ┌─────────────────────────┐
│  PHYSICAL QR     │        │  MOBILE PHONE CAMERA    │
│  CODE (Printed)  │───────→│  (Built-in Scanner)     │
│  or URL Link     │        │                         │
└──────────────────┘        └────────────┬────────────┘
                                         │
                                         ↓
                          ┌──────────────────────────┐
                          │  QR Code Scanned         │
                          │  URL Detected            │
                          │  https://...../qr/...    │
                          └────────────┬─────────────┘
                                       │
                                       ↓
                          ┌──────────────────────────┐
                          │  Browser Opens URL       │
                          │  Loads Form Page         │
                          └────────────┬─────────────┘
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
                 ↓                                           ↓
    ┌──────────────────────────┐          ┌──────────────────────────┐
    │   ROOM ADDITION FORM      │          │ RESIDENT ADDITION FORM   │
    │  /qr/room/form/<pg_id>/  │          │/qr/resident/form/<rm_id>/│
    ├──────────────────────────┤          ├──────────────────────────┤
    │ • Room Number            │          │ • Name                   │
    │ • Capacity               │          │ • Age                    │
    │ • Rent                   │          │ • Gender                 │
    │ • [Submit Button]        │          │ • Mobile Number          │
    └────────────┬─────────────┘          │ • Address                │
                 │                         │ • Photo (Optional)       │
                 │                         │ • [Submit Button]        │
                 │                         └────────────┬─────────────┘
                 │                                      │
                 └──────────────────┬───────────────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                          ↓                   ↓
                  ┌─────────────────┐  ┌─────────────────┐
                  │  FORM SUBMITTED │  │  VALIDATION     │
                  │                 │  │  • Check fields │
                  │  Data Sent to   │  │  • Check files  │
                  │  Server         │  │  • Save to DB   │
                  └────────┬────────┘  └────────┬────────┘
                           │                    │
                           └──────────┬─────────┘
                                      │
                           ┌──────────┴──────────┐
                           │                     │
                           ↓                     ↓
                  ┌──────────────────┐  ┌──────────────────┐
                  │  ROOM CREATED    │  │RESIDENT CREATED  │
                  │  ✓ Record Saved  │  │✓ Record Saved    │
                  │  ✓ ID Generated  │  │✓ ID Generated    │
                  └────────┬─────────┘  └────────┬─────────┘
                           │                     │
                           └──────────┬──────────┘
                                      │
                                      ↓
                           ┌──────────────────────┐
                           │  SUCCESS PAGE SHOWN  │
                           │                      │
                           │ ✓ Record Created     │
                           │ • Details Display    │
                           │ • Go Back Button     │
                           │ • Home Button        │
                           │                      │
                           │ [Go to Home]         │
                           │ [Go Back]            │
                           └──────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                         MULTI-QR GRID VIEWS
═══════════════════════════════════════════════════════════════════════════

PG DETAIL PAGE
    │
    └─→ "View All Room QR Codes" ─→ PG_ROOMS_QR PAGE
                                     │
                                     ├─→ Room 1 [QR] [View QR] [Details]
                                     │
                                     ├─→ Room 2 [QR] [View QR] [Details]
                                     │
                                     ├─→ Room 3 [QR] [View QR] [Details]
                                     │
                                     └─→ Room N [QR] [View QR] [Details]


ROOM DETAIL PAGE
    │
    └─→ "View Resident QR Codes" ─→ ROOM_RESIDENTS_QR PAGE
                                    │
                                    ├─→ Resident 1 [QR] [View QR] [Edit]
                                    │
                                    ├─→ Resident 2 [QR] [View QR] [Edit]
                                    │
                                    ├─→ Resident 3 [QR] [View QR] [Edit]
                                    │
                                    └─→ Resident N [QR] [View QR] [Edit]


═══════════════════════════════════════════════════════════════════════════
                        DATA FLOW & STRUCTURE
═══════════════════════════════════════════════════════════════════════════

ADMIN CREATES ROOM
    │
    ├─→ Form Data: room_number, capacity, rent
    │
    ├─→ Django saves to database
    │
    ├─→ room_qr_code() view called
    │   ├─→ Generates URL: /qr/room/form/<pg_id>/
    │   ├─→ Encodes URL in QR (qrcode library)
    │   ├─→ Returns base64 PNG image
    │   └─→ Renders room_qr_code.html template
    │
    └─→ Shows to admin with:
        ├─ QR Code Image
        ├─ Form URL
        ├─ Print Button
        └─ Copy URL Button


OTHERS SCAN QR & ADD ROOM
    │
    ├─→ Scan QR Code with phone camera
    │
    ├─→ URL opened: /qr/room/form/<pg_id>/
    │
    ├─→ scan_qr_room_form() view processes
    │   ├─→ GET request: Renders form template
    │   │   └─ scan_qr_room_form.html
    │   │
    │   └─→ POST request: Processes submission
    │       ├─ Validates form data
    │       ├─ Creates Room record
    │       ├─ Saves to database
    │       └─ Shows qr_room_success.html
    │
    └─→ Success page shows:
        ├─ ✓ Success message
        ├─ Room details
        ├─ Navigation buttons
        └─ Celebration animation


═══════════════════════════════════════════════════════════════════════════
                        URL ENDPOINTS MAPPING
═══════════════════════════════════════════════════════════════════════════

ADMIN-ONLY (Login Required)
─────────────────────────────────────────────────────────────────────────
GET    /                              → home() - Admin Dashboard
GET    /add-pg/                       → add_pg() - Create PG
POST   /add-pg/                       → add_pg() - Save PG
GET    /pg/<pg_id>/                   → pg_detail() - View PG
GET    /pg/<pg_id>/add-room/          → add_room() - Add Room Form
POST   /pg/<pg_id>/add-room/          → add_room() - Save Room
GET    /room/<room_id>/               → room_detail() - View Room
GET    /room/<room_id>/add-resident/  → add_resident() - Add Resident
POST   /room/<room_id>/add-resident/  → add_resident() - Save Resident

QR DISPLAY (Admin)
─────────────────────────────────────────────────────────────────────────
GET    /room/<room_id>/qr/            → room_qr_code() - Show Room QR
GET    /resident/<resident_id>/qr/    → resident_qr_code() - Show Res QR
GET    /pg/<pg_id>/rooms-qr/          → pg_rooms_with_qr() - Grid View
GET    /room/<room_id>/residents-qr/  → room_residents_with_qr() - Grid

PUBLIC (No Login - Accessed via QR)
─────────────────────────────────────────────────────────────────────────
GET    /qr/room/form/<pg_id>/         → scan_qr_room_form() - Room Form
POST   /qr/room/form/<pg_id>/         → scan_qr_room_form() - Submit
GET    /qr/resident/form/<room_id>/   → scan_qr_resident_form() - Res Form
POST   /qr/resident/form/<room_id>/   → scan_qr_resident_form() - Submit


═══════════════════════════════════════════════════════════════════════════
                      TECHNOLOGY STACK
═══════════════════════════════════════════════════════════════════════════

Backend:
  • Django (Python Web Framework)
  • python-qrcode (QR Generation)
  • SQLite (Database)
  • Django Forms (Form Handling)

Frontend:
  • HTML5 (Structure)
  • CSS3 (Styling)
  • JavaScript (Interactivity)
  • Font Awesome (Icons)
  • Responsive Design (Mobile-First)

Security:
  • Django CSRF Protection
  • Form Validation
  • Context-Specific URLs
  • No Sensitive Data in QR

Performance:
  • Base64 Encoded QR (No extra requests)
  • Cached Form Pages
  • Optimized Mobile Rendering
  • Fast QR Generation


═══════════════════════════════════════════════════════════════════════════
                      DEPLOYMENT STRUCTURE
═══════════════════════════════════════════════════════════════════════════

/pg_management/
├── pgapp/
│   ├── views.py              ← Updated with new views
│   ├── urls.py               ← Added new URL patterns
│   ├── qr_utils.py           ← Simplified QR generation
│   ├── models.py             ← Unchanged
│   ├── forms.py              ← Unchanged
│   └── templates/
│       ├── room_qr_code.html          ← Updated (URL-based)
│       ├── resident_qr_code.html      ← Updated (URL-based)
│       ├── scan_qr_room_form.html     ← New (Public)
│       ├── scan_qr_resident_form.html ← New (Public)
│       ├── qr_room_success.html       ← New (Success)
│       ├── qr_resident_success.html   ← New (Success)
│       ├── pg_rooms_qr.html           ← Updated (Dict structure)
│       └── room_residents_qr.html     ← Updated (Dict structure)
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
└── Documentation/
    ├── QR_ENHANCEMENT_GUIDE.md        ← Complete Feature Guide
    ├── QR_CHANGES_SUMMARY.md          ← Technical Details
    ├── IMPLEMENTATION_CHECKLIST.md    ← Testing Checklist
    ├── QUICK_START_QR.md              ← Quick Reference
    └── QR_SYSTEM_ARCHITECTURE.md      ← This file


═══════════════════════════════════════════════════════════════════════════
                      BENEFITS VISUALIZATION
═══════════════════════════════════════════════════════════════════════════

BEFORE (Old Data-Based QR)
────────────────────────────
  QR Code Contains: {type: room, pg_id: 1, ...}
                    │
                    ↓ Requires complex decoder
                    
  Problems:
  ✗ Only works with custom app
  ✗ Not mobile-friendly
  ✗ Complex for users
  ✗ Data encoding overhead
  ✗ Limited to predefined fields


AFTER (New URL-Based QR) ✓
──────────────────────────
  QR Code Contains: https://yourdomain.com/qr/room/form/1/
                    │
                    ↓ Any QR scanner works!
                    
  Benefits:
  ✓ Works with ANY phone
  ✓ Beautiful mobile forms
  ✓ Simple for anyone
  ✓ Light weight
  ✓ Extensible design
  ✓ Professional UI
  ✓ Shareable URLs


═══════════════════════════════════════════════════════════════════════════

Generated: January 30, 2026
Version: 2.0
Status: Production Ready ✅
