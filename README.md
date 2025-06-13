# VulnTrack Backend - Advanced Device Vulnerability Management System

## Overview

VulnTrack Backend is a comprehensive FastAPI application designed for managing firewall devices with advanced vulnerability scanning capabilities. This system provides enterprise-grade device management combined with intelligent vulnerability detection using multiple data sources and AI-powered analysis.

## 🔥 Key Features

### Device Management
- **Create, Read, Update, Delete** firewall devices
- **Search and Filter** devices by name, brand, model, version, location
- **Version Tracking** for firmware management
- **Device Activation/Deactivation** (soft delete)
- **Unique Constraints** on hostname and serial number
- **Pagination** for large device inventories

### 🛡️ Advanced Vulnerability Scanning
- **Hybrid Vulnerability Detection** using multiple sources
- **Local CVE Database** integration (MongoDB)
- **AI-Powered Analysis** with Gemini AI direct knowledge
- **Web Search Integration** with Brave Search API
- **Automatic Result Filtering** using regex and keyword detection
- **Intelligent Source Validation** for trusted security sources
- **Real-time Vulnerability Assessment** with confidence scoring
- **CVE Detection and Mapping** with CVSS scoring

### 🎯 Vulnerability Scanning Pipeline
1. **Local CVE Database Check** - MongoDB vulnerability lookup
2. **Gemini AI Direct Knowledge** - AI-based vulnerability assessment
3. **Filtered Web Search** - Brave Search with automatic filtering
4. **AI Result Validation** - Gemini AI analysis of search results
5. **Confidence Scoring** - Multi-source confidence assessment

### Device Properties
Each device includes:
- `id`: UUID primary key
- `name`: Device name/identifier
- `hostname`: Network hostname (unique)
- `version`: Firmware/software version
- `brand`: Device manufacturer
- `model`: Device model
- `serial_number`: Hardware serial number (unique)
- `location`: Physical/logical location
- `user_id`: Responsible user UUID
- `is_active`: Active status flag
- `created_at`/`updated_at`: Audit timestamps

### API Endpoints

#### Device Management
- `POST /api/v1/devices/` - Create new device
- `GET /api/v1/devices/` - List devices (with pagination/filtering)
- `GET /api/v1/devices/{id}` - Get specific device
- `PUT /api/v1/devices/{id}` - Update device
- `DELETE /api/v1/devices/{id}` - Delete device permanently
- `PATCH /api/v1/devices/{id}/deactivate` - Deactivate device
- `GET /api/v1/devices/search/by-name` - Search by name
- `GET /api/v1/devices/search/by-version` - Search by version
- `GET /api/v1/devices/search/by-brand` - Search by brand/model
- `GET /api/v1/devices/search/general` - General search
- `GET /api/v1/devices/versions/summary` - Version distribution summary
- `GET /api/v1/devices/versions/list` - Detailed version information

#### 🔍 Vulnerability Scanning
- `POST /api/v1/vulnerabilities/scan/device/{device_id}` - Scan specific device
- `POST /api/v1/vulnerabilities/scan/bulk` - Bulk scan multiple devices
- `GET /api/v1/vulnerabilities/scan/status/{scan_id}` - Get scan status
- `POST /api/v1/vulnerabilities/scan/device/{device_id}/quick` - Quick scan for specific device
- `GET /api/v1/vulnerabilities/reports/device/{device_id}` - Device vulnerability report (pending)
- `GET /api/v1/vulnerabilities/reports/summary` - Organization-wide vulnerability summary (pending)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (primary storage)
- MongoDB database (CVE database)
- Poetry for dependency management
- Gemini AI API key
- Brave Search API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vulntrack-backend
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   # Application Configuration
   APP_PORT=8000
   ENVIRONMENT=development

   # Database Configuration (PostgreSQL)
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=user
   DB_PASSWORD=password
   DB_NAME=analyzer-db
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/analyzer-db

   # MongoDB Configuration (CVE Database)
   MONGODB_HOST=localhost
   MONGODB_PORT=27017
   MONGODB_USER=user
   MONGODB_PASSWORD=password
   MONGODB_DB_NAME=cve_db
   MONGODB_URL=mongodb://user:password@localhost:27017/?authSource=admin

   # Gemini AI API Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
   GEMINI_MAX_TOKENS=2048
   GEMINI_TEMPERATURE=0.1

   # Brave Search API Configuration
   BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here
   BRAVE_SEARCH_BASE_URL=https://api.search.brave.com/res/v1
   BRAVE_SEARCH_COUNT=10
   BRAVE_SEARCH_COUNTRY=US
   BRAVE_SEARCH_SEARCH_LANG=en
   BRAVE_SEARCH_UI_LANG=en-US

   # Vulnerability Scanning Settings
   VULN_SCAN_ENABLED=true
   VULN_SCAN_TIMEOUT=30
   VULN_SCAN_MAX_RETRIES=3
   VULN_SCAN_CACHE_TTL=3600
   VULN_SCAN_BATCH_SIZE=5
   VULN_SCAN_RATE_LIMIT_DELAY=1.0
   ```

4. **Set up the databases:**
   ```bash
   # PostgreSQL: Create database tables using Alembic
   poetry run alembic upgrade head
   
   # MongoDB: Ensure CVE database is running and accessible
   # Alternative: Use SQLite for development
   poetry run python scripts/setup_sqlite.py
   ```

5. **Run the application:**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

6. **Access the API:**
   - API Documentation: http://127.0.0.1:8000/docs
   - Alternative Docs: http://127.0.0.1:8000/redoc
   - API Base URL: http://127.0.0.1:8000/api/v1

## 🧪 Testing

### Vulnerability Scanning Tests
Run the comprehensive vulnerability scanning test suite:
```bash
poetry run pytest tests/unit/test_vulnerability_scanning.py -v
```

### Automated API Testing
Run the complete test suite:
```bash
poetry run python test_api.py
```

### Unit Tests
Run all unit tests:
```bash
poetry run pytest
```

### Manual Testing
Use the interactive API documentation at `/docs` to test endpoints manually.

## 📊 Usage Examples

### Creating a Firewall Device
```python
import requests
import uuid

device_data = {
    "name": "Firewall-DMZ-01",
    "hostname": "fw-dmz-01.company.com", 
    "version": "9.1.5",
    "brand": "Palo Alto Networks",
    "model": "PA-3220",
    "serial_number": "001234567890",
    "location": "Data Center - DMZ",
    "user_id": str(uuid.uuid4()),
    "is_active": True
}

response = requests.post("http://localhost:8000/api/v1/devices/", json=device_data)
print(response.json())
```

### 🔍 Scanning Device for Vulnerabilities
```python
# Scan a specific device
device_id = "123e4567-e89b-12d3-a456-426614174000"
response = requests.post(f"http://localhost:8000/api/v1/vulnerabilities/scan/device/{device_id}")
scan_result = response.json()

print(f"Vulnerabilities found: {scan_result['scan_result']['vulnerabilities_found']}")
print(f"Scan methods used: {scan_result['scan_result']['methods_used']}")
print(f"Confidence score: {scan_result['scan_result']['confidence_score']}")
```

### 📈 Bulk Vulnerability Scanning
```python
# Scan multiple devices
scan_request = {
    "device_ids": [
        "123e4567-e89b-12d3-a456-426614174000",
        "987fcdeb-51d2-43e8-9012-345678901234"
    ],
    "scan_options": {
        "include_low_confidence": False,
        "max_concurrent": 3
    }
}

response = requests.post("http://localhost:8000/api/v1/vulnerabilities/scan/bulk", json=scan_request)
bulk_results = response.json()
```

### 📊 Vulnerability Reporting
```python
# Get device vulnerability report
device_id = "123e4567-e89b-12d3-a456-426614174000"
response = requests.get(f"http://localhost:8000/api/v1/vulnerabilities/reports/device/{device_id}")
report = response.json()

# Get organization-wide summary
response = requests.get("http://localhost:8000/api/v1/vulnerabilities/reports/summary")
summary = response.json()
```

### Searching Devices by Version
```python
response = requests.get("http://localhost:8000/api/v1/devices/search/by-version?version=9.1.5")
devices = response.json()
```

## 🏗️ Project Structure

```
vulntrack-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/v1/              # API version 1
│   │   ├── api.py           # API router configuration
│   │   └── endpoints/       # API endpoints
│   │       ├── devices.py   # Device management endpoints
│   │       └── vulnerability.py # Vulnerability scanning endpoints
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   │   └── device.py        # Device data model
│   ├── schemas/             # Pydantic schemas
│   │   ├── device.py        # Device validation schemas
│   │   └── vulnerability.py # Vulnerability response schemas
│   └── services/            # Business logic
│       ├── device_service.py       # Device management service
│       ├── cve_service.py          # CVE database service
│       ├── external_apis.py        # Brave Search & Gemini AI
│       └── vulnerability_scanner.py # Main vulnerability scanner
├── alembic/                 # Database migrations
├── tests/                   # Test files
│   ├── unit/               # Unit tests
│   │   └── test_vulnerability_scanning.py # Vulnerability tests
│   └── api/                # API integration tests
├── scripts/                # Utility scripts
│   ├── init_db.py         # Database initialization
│   └── setup_sqlite.py    # SQLite setup for development
├── cve-local/             # Local CVE data management
├── docs/                  # Documentation
└── pyproject.toml         # Project configuration
```

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - ORM with declarative base
- **Pydantic v2** - Data validation and serialization
- **Uvicorn** - ASGI server

### Databases
- **PostgreSQL** - Primary application database
- **MongoDB** - CVE vulnerability database
- **SQLite** - Development database fallback

### Vulnerability Scanning
- **Gemini AI** - Google's AI for vulnerability analysis
- **Brave Search API** - Web search for vulnerability information
- **PyMongo** - MongoDB driver for CVE data
- **httpx** - Async HTTP client for API calls

### Development Tools
- **Poetry** - Dependency management
- **Alembic** - Database migrations
- **Pytest** - Testing framework
- **pytest-asyncio** - Async testing support

## 🔧 Configuration

The application uses environment-based configuration. Key settings:

### Application Settings
- `APP_PORT`: Application port (default: 8000)
- `ENVIRONMENT`: Runtime environment (development/production)

### Database Configuration
- `DB_*`: PostgreSQL connection parameters
- `DATABASE_URL`: Complete PostgreSQL connection string
- `MONGODB_*`: MongoDB CVE database connection parameters

### AI & Search APIs
- `GEMINI_API_KEY`: Google Gemini AI API key
- `GEMINI_MODEL`: AI model to use (default: gemini-1.5-flash)
- `BRAVE_SEARCH_API_KEY`: Brave Search API key
- `BRAVE_SEARCH_*`: Search API configuration parameters

### Vulnerability Scanning
- `VULN_SCAN_ENABLED`: Enable/disable vulnerability scanning
- `VULN_SCAN_TIMEOUT`: API request timeout (seconds)
- `VULN_SCAN_MAX_RETRIES`: Maximum retry attempts
- `VULN_SCAN_CACHE_TTL`: Cache time-to-live (seconds)

## 🗄️ Database Schema

### PostgreSQL - Devices Table
```sql
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    hostname VARCHAR(255) NOT NULL UNIQUE,
    version VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### MongoDB - CVE Database
```javascript
// CVE Collection Structure
{
  "_id": ObjectId,
  "cve": {
    "CVE_data_meta": {
      "ID": "CVE-2024-XXXX"
    },
    "description": {
      "description_data": [{
        "value": "Vulnerability description"
      }]
    },
    "impact": {
      "baseMetricV3": {
        "cvssV3": {
          "baseSeverity": "High",
          "baseScore": 8.5
        }
      }
    }
  }
}
```

## 🚦 API Response Examples

### Vulnerability Scan Response
```json
{
  "success": true,
  "message": "Vulnerability scan completed",
  "scan_result": {
    "device_info": {
      "brand": "Palo Alto Networks",
      "model": "PA-220",
      "version": "9.1.3"
    },
    "scan_timestamp": "2025-06-13T08:55:14.573045",
    "vulnerabilities_found": true,
    "vulnerability_count": 3,
    "methods_used": [
      "local_cve_database",
      "direct_ai_knowledge",
      "web_search_filtered"
    ],
    "confidence_score": 0.9,
    "scan_duration_seconds": 6.68,
    "scan_results": {
      "local_cve": {
        "vulnerabilities_found": false,
        "vulnerability_count": 0
      },
      "ai_direct": {
        "vulnerabilities_found": true,
        "confidence_level": "high",
        "vulnerabilities": [
          {
            "cve_id": "CVE-2024-0012",
            "severity": "Critical",
            "cvss_score": "9.3",
            "description": "Authentication bypass vulnerability"
          }
        ]
      },
      "web_search": {
        "total_raw_results": 24,
        "filtered_results_count": 10
      }
    }
  }
}
```

### Device Creation Response
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Firewall-DMZ-01",
    "hostname": "fw-dmz-01.company.com",
    "version": "9.1.5",
    "brand": "Palo Alto Networks", 
    "model": "PA-3220",
    "serial_number": "001234567890",
    "location": "Data Center - DMZ",
    "user_id": "987fcdeb-51d2-43e8-9012-345678901234",
    "is_active": true,
    "created_at": "2025-06-11T10:30:00Z",
    "updated_at": "2025-06-11T10:30:00Z"
}
```

## 🔮 Future Enhancements

### Completed Features ✅
- **Advanced Vulnerability Scanning** with hybrid AI approach
- **Multi-source Intelligence** (CVE DB + AI + Web Search)
- **Automatic Result Filtering** and validation
- **Real-time Confidence Scoring** for vulnerability assessments

### Planned Features 🚧
- **Compliance Reporting** features (SOC2, ISO27001, NIST)
- **Device Grouping** and advanced tagging system
- **Automated Discovery** capabilities via SNMP/SSH
- **Integration APIs** for SIEM and monitoring tools
- **Audit Logging** for all changes and scans
- **Role-based Access Control** (RBAC)
- **Device Configuration** backup/restore
- **Vulnerability Trend Analysis** and dashboards
- **Automated Patch Management** integration
- **Custom Vulnerability Rules** and thresholds
- **Multi-tenant Support** for MSPs
- **Advanced Reporting** with PDF/Excel export

### CI/CD Integration 🔄
- **Automated Testing Pipeline** with pytest
- **Security Scanning** in CI/CD
- **Container Deployment** with Docker
- **Kubernetes Orchestration** support
- **Performance Monitoring** and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Built with ❤️ for network security professionals**