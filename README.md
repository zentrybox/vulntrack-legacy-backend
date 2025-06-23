# VulnTrack Core Scanning Engine

## Overview

VulnTrack Core Scanning Engine es un backend minimalista para orquestar el escaneo de vulnerabilidades en dispositivos, usando Supabase como fuente de datos y gestionando la lógica de escaneo, integración con Gemini AI y Brave Search.

## 🚀 Arquitectura Minimalista
- **Sin base de datos local**: Todos los datos CRUD (dispositivos, usuarios, resultados) se gestionan en Supabase.
- **Solo lógica de escaneo**: El backend solo ejecuta el pipeline de escaneo y análisis.
- **Integración con APIs externas**: Gemini AI y Brave Search para análisis y enriquecimiento.

## 🔑 Características Principales
- **Obtención de dispositivos desde Supabase** (API REST vía httpx)
- **Escaneo híbrido**: Gemini AI + Brave Search
- **Resultados y reportes enviados a Supabase**
- **Configuración por variables de entorno** (solo APIs externas y parámetros de escaneo)

## ✂️ Elementos eliminados
- Gestión local de dispositivos, usuarios, reportes, historial, etc.
- Integración y migraciones de PostgreSQL/MongoDB/SQLite
- Endpoints CRUD y lógica de negocio de gestión
- Dependencias de SQLAlchemy, Alembic, PyMongo, supabase-py, etc.

## ⚡ Endpoints disponibles
- `POST /api/v1/vulnerabilities/scan/device/{device_id}` - Escaneo híbrido (Supabase → AI)
- `POST /api/v1/vulnerabilities/scan/devices/batch` - Escaneo batch
- `GET /api/v1/vulnerabilities/scan/status` - Estado/configuración del motor

## ⚙️ Configuración mínima (`.env`)
```env
APP_PORT=8000
ENVIRONMENT=development
SUPABASE_URL=https://domain-project.supabase.co
SUPABASE_KEY=input-your-key-here
GEMINI_API_KEY=tu_gemini_api_key
GEMINI_MODEL=gemini-model
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.1
BRAVE_SEARCH_API_KEY=tu_brave_api_key
BRAVE_SEARCH_BASE_URL=https://api.search.brave.com/res/v1
BRAVE_SEARCH_COUNT=10
VULN_SCAN_ENABLED=true
VULN_SCAN_TIMEOUT=30
VULN_SCAN_MAX_RETRIES=3
VULN_SCAN_CACHE_TTL=3600
VULN_SCAN_BATCH_SIZE=5
VULN_SCAN_RATE_LIMIT_DELAY=1.0
```

## 🛠️ Stack Tecnológico
- **FastAPI** (API)
- **httpx** (cliente REST para Supabase)
- **Gemini AI** (Google)
- **Brave Search API**

## 📝 Notas
- Toda la gestión de datos (CRUD) se realiza en Supabase vía API REST.
- El backend solo orquesta el escaneo y análisis.
- Elimina cualquier referencia a DB local, migraciones, scripts de setup, endpoints CRUD, y dependencias de DB o SDKs inestables.

---
**Built for modern, serverless vulnerability scanning.**