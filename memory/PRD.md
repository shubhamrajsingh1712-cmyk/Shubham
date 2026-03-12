# BoatMyCareer.com - Product Requirements Document

## Problem Statement
Build "BoatMyCareer.com," a comprehensive career counseling platform for students in Class VII to XII, founded by Shubham Raj Singh. Pricing: ₹999 primary program, ₹1000 for 1-year extended guidance.

## Core Architecture
- **Backend**: FastAPI + MongoDB + JWT Auth
- **Frontend**: React + Tailwind CSS + Shadcn UI
- **PDF Reports**: ReportLab

## What's Been Implemented

### Phase 1: Core Platform (Completed)
- Student & Admin JWT authentication
- Student/Admin dashboards
- Payment page (MOCKED - UPI placeholder)
- Landing page with all sections

### Phase 2: Psychometric Assessment (Completed)
- 200-question bank across 5 dimensions
- Full assessment UI flow with answer tracking
- Partial submission support
- Advanced scoring engine (`scoring_engine.py`)
- Multi-page PDF report generator (`report_generator.py`)

### Phase 3: Career Library (Completed - March 2026)
- **281 careers** across **14 categories**
- Backend API: search, filter by category, pagination, detail view
- Frontend: CareerLibraryPage (grid + sidebar filters + search)
- Frontend: CareerDetailPage (full info: education, salary, skills, exams, institutions, pros/challenges)
- Landing page category cards link to filtered library
- "Explore All Careers" button links to /careers

### Deployment Readiness (Completed - March 2026)
- Removed hardcoded JWT_SECRET_KEY fallback
- Added JWT_SECRET_KEY to backend/.env
- Admin user created with proper fields

## Key DB Collections
- **users**: id, name, email, password, role, payment_status, created_at
- **tests**: user_id, test_type, responses, score_details, created_at
- **reports**: user_id, report_id, file_path, generated_at, report_data

## Key API Endpoints
- `POST /api/auth/register` / `POST /api/auth/login` / `GET /api/auth/me`
- `GET /api/questions/{test_type}` / `POST /api/tests/submit`
- `POST /api/reports/generate` / `GET /reports/{report_id}`
- `GET /api/careers/categories` / `GET /api/careers/search` / `GET /api/careers/{slug}`
- `GET /api/admin/users` / `GET /api/admin/payments` / `GET /api/admin/reports`

## Credentials
- Admin: admin@boatmycareer.com / admin123

## Prioritized Backlog

### P1 - High Priority
- Populate career library to 400+ careers (currently 281)
- Integrate assessment report with career library (link recommendations to career pages)

### P2 - Medium Priority
- Payment gateway integration (replace MOCKED UPI placeholder)
- One-on-One Counselling booking system
- Extended Guidance Program (Stage 5)

### P3 - Low Priority / Refactoring
- Refactor LandingPage.js (800+ lines) into smaller components
- Refactor server.py into separate router modules
- Add career editing via admin dashboard
