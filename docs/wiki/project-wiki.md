# VulnTrack Project Wiki

---

## 1. Overview

VulnTrack is a modern, full-stack vulnerability management platform designed for organizations that require robust, AI-powered vulnerability scanning, reporting, and device management. It consists of two main components:

- **VulnTrack Vulnerability Scanner Engine** (backend, Python/FastAPI)
- **VulnTrack Frontend** (Next.js/TypeScript)

Both components use **Supabase** as the single source of truth for all data, authentication, and notifications.

---

## 2. Architecture

- **Backend**: Stateless FastAPI app, all data via Supabase REST API (httpx)
- **Frontend**: Next.js (App Router), TypeScript, ShadCN/UI, Tailwind CSS
- **AI Integration**: Google Gemini (backend), Google Genkit (frontend)
- **Async Processing**: Celery + Redis (backend)
- **Monitoring**: Flower (backend), Firebase Hosting (frontend)
- **Database**: Supabase (Postgres + Auth)
- **Containerization**: Docker & docker-compose for backend

---

## 3. Backend: Vulnerability Scanner Engine

### 3.1. Features
- Stateless, minimal, robust Python backend
- All CRUD and persistence via Supabase REST API
- Orchestrates device scans, AI analysis, and reporting
- Asynchronous scan processing with Celery + Redis
- AI-powered summaries and remediation (Google Gemini)
- RESTful, well-documented endpoints (OpenAPI/Swagger)
- Batch and single scan support
- Notification and activity logging
- Containerized for easy deployment

### 3.2. API Endpoints
- `POST /api/v1/` — Trigger scan for a device
- `POST /api/v1/batch` — Batch scan
- `GET /api/v1/scan/{scan_id}` — Scan status/results
- `GET /api/v1/scan/status` — Engine status/config

### 3.3. Data Flow
- All data (devices, scans, results, notifications) in Supabase
- No local DB, no ORM, no migrations
- AI fields stored in scans/scan_results
- All user management via Supabase Auth

### 3.4. Async Processing
- Celery for background scan/AI jobs
- Redis as broker
- Flower for monitoring (port 5555)

### 3.5. Deployment
- Dockerfile and docker-compose.yml provided
- Services: api, worker, flower, redis
- All config via .env and docker-compose

---

## 4. Frontend: VulnTrack Web App

### 4.1. Features
- Built with Next.js (App Router) and TypeScript
- UI: ShadCN/UI, Tailwind CSS, custom theming (light/dark)
- Supabase as DB client (all data, auth, notifications)
- Google Genkit for AI-powered flows (summaries, remediation, recommendations)
- Device management: create, edit, view, scan
- Scan history, dashboard, PDF/CSV export
- Anti-corruption layer: maps Supabase snake_case to frontend camelCase
- Authentication via Supabase Auth (middleware, login page)
- Database seeding via UI
- Test console for dev/test data
- Firebase App Hosting ready

### 4.2. Project Structure
```
.
├── src/
│   ├── app/                # App routes (pages)
│   ├── ai/                 # Genkit AI integration
│   ├── components/         # UI and common components
│   ├── config/             # App config
│   ├── hooks/              # Custom hooks
│   ├── lib/                # API, Supabase client, utils
│   └── types/              # TypeScript types
├── docs/                   # Documentation
├── public/                 # Static assets
└── ...                     # Config files
```

### 4.3. Core Pages
- **Dashboard**: Org security overview, stats, charts
- **Devices**: List, filter, create/edit, scan
- **Device Details**: Scan history, AI summaries, remediation, export
- **Scan History**: All scans, filters
- **Test Console**: Dev/test data generation

### 4.4. AI Integration
- Google Genkit flows in `src/ai/flows/`
- Used for remediation, summaries, recommendations
- Configured in `src/ai/genkit.ts`

### 4.5. Theming
- Tailwind CSS utility-first
- CSS variables for light/dark themes
- ThemeProvider and ThemeToggle for user switching

### 4.6. Deployment
- Firebase App Hosting
- Config in `apphosting.yaml`

---

## 5. Supabase Integration (Shared)

- All data (devices, scans, results, notifications, users) in Supabase
- Supabase Auth for authentication and user management
- REST API for backend, JS client for frontend
- Shared schema, single source of truth
- Environment variables for all secrets/keys

---

## 6. Security & Best Practices

- Never expose service role keys or secrets in the frontend
- All data access via Supabase REST API with proper API keys
- Use HTTPS and secure .env files in production
- Monitor Celery, Redis, and Flower for backend health
- Use Supabase Auth for all user/session management

---

## 7. Troubleshooting

- **Scan not completing?** Check worker and Redis logs
- **No AI results?** Check Gemini/Genkit API keys and quotas
- **No notifications?** Ensure user_id is set and notifications table is configured
- **400 Bad Request from Supabase?** Check payload fields/types against schema

---

## 8. References

- [Supabase Docs](https://supabase.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Celery Docs](https://docs.celeryq.dev/)
- [Flower Docs](https://flower.readthedocs.io/)
- [Google Gemini](https://ai.google.dev/gemini)
- [Google Genkit](https://firebase.google.com/docs/genkit)
- [Next.js Docs](https://nextjs.org/docs)
- [ShadCN/UI](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Docker Compose](https://docs.docker.com/compose/)
