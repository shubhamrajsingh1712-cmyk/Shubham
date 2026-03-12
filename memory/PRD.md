# BoatMyCareer.com - Product Requirements Document

## Problem Statement
Build "BoatMyCareer.com," a comprehensive career counseling platform for students in Class VII to XII, founded by Shubham Raj Singh. Pricing: ₹999 primary program, ₹1000 for 1-year extended guidance.

## Core Architecture
- **Backend**: FastAPI + MongoDB + JWT Auth
- **Frontend**: React + Tailwind CSS + Shadcn UI
- **PDF Reports**: ReportLab + Matplotlib

## What's Been Implemented

### Phase 1: Core Platform (Completed)
- Student & Admin JWT authentication
- Student/Admin dashboards
- Payment page (MOCKED - UPI placeholder)
- Landing page with all sections

### Phase 2: Psychometric Assessment (Completed)
- 200-question bank across 5 dimensions (30 traits total)
- Full assessment UI flow with answer tracking
- Partial submission support
- Advanced scoring engine (`scoring_engine.py`)

### Phase 3: Comprehensive Report Generator (Completed - March 2026)
- **23-page detailed PDF report** (was 13 pages with blank pages)
- Cover page with student info + Framework Introduction page
- Executive Summary with 5-dimensional radar chart
- **5 full dimension sections** each with:
  - "What is [Dimension]?" introduction
  - Dominant traits summary
  - Bar chart visualization
  - **Trait-by-trait detailed analysis** (30 traits total):
    - Meaning (what the trait measures)
    - Expert Analysis (personalized based on score band: High/Moderate/Low)
    - Development Plan (actionable bullet points)
- Career Recommendations section with top 5 matches (linked to Career Library data)
- Strengths & Development Roadmap with 90-day action plan
- Appendix with score band reference + disclaimer

### Phase 4: Career Library (Completed - March 2026)
- **281 careers** across **14 categories**
- Backend API: search, filter by category, pagination, detail view
- Frontend: CareerLibraryPage (grid + sidebar filters + search)
- Frontend: CareerDetailPage (salary, skills, education, exams, institutions, pros/challenges)
- Landing page category cards link to filtered library

### Deployment Readiness (Completed - March 2026)
- Removed hardcoded JWT_SECRET_KEY fallback
- Added JWT_SECRET_KEY to backend/.env
- Admin user created with proper fields

## Key DB Collections
- **users**: id, name, email, password, role, payment_status, created_at
- **test_results**: user_id, test_type, responses, scores, scoring_details, created_at
- **reports**: id, user_id, test_results, overall_scores, career_recommendations, strengths, development_areas, report_file_path, generated_at

## Key API Endpoints
- Auth: `POST /api/auth/register` | `POST /api/auth/login` | `GET /api/auth/me`
- Tests: `GET /api/questions/{test_type}` | `POST /api/tests/submit`
- Reports: `POST /api/reports/generate/{user_id}` | `GET /api/reports/download/{report_id}`
- Careers: `GET /api/careers/categories` | `GET /api/careers/search` | `GET /api/careers/{slug}`
- Admin: `GET /api/admin/users` | `GET /api/admin/payments` | `GET /api/admin/reports`

## Credentials
- Admin: admin@boatmycareer.com / admin123

## Prioritized Backlog

### Landing Page Restructuring (Completed - March 2026)
- Simplified Sample Report section to a single download button linking to `/sample_report.pdf`
- Removed Career Library section from landing page body (nav link retained, points to `/careers`)
- Moved "Meet Your Career Guide" section to be last before footer

### P0 - Next Priority
- Integrate Assessment Report with Career Library (link recommendations to career pages)

### P1 - High Priority
- Populate career library to 400+ careers
- Integrate assessment report with career library (clickable links from report to career pages)

### P2 - Medium Priority
- Payment gateway integration (replace MOCKED UPI placeholder)
- One-on-One Counselling booking system
- Extended Guidance Program (Stage 5)

### P3 - Low Priority / Refactoring
- Refactor LandingPage.js (800+ lines) into smaller components
- Refactor server.py into separate router modules
- Add career editing via admin dashboard
