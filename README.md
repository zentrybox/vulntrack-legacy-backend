# VulnTrack Backend - Device Management System

## Overview

VulnTrack Backend is a FastAPI application designed for managing firewall devices with a focus on version management and vulnerability tracking. This system provides comprehensive CRUD operations for device management, making it ideal for network administrators and security teams.

## 🔥 Key Features

### Device Management
- **Create, Read, Update, Delete** firewall devices
- **Search and Filter** devices by name, brand, model, version, location
- **Version Tracking** for firmware management
- **Device Activation/Deactivation** (soft delete)
- **Unique Constraints** on hostname and serial number
- **Pagination** for large device inventories

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

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Poetry for dependency management

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
   ```

4. **Set up the database:**
   ```bash
   # Create database tables using Alembic
   poetry run alembic upgrade head
   
   # Alternative: Create tables directly
   poetry run python init_db.py
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

### Automated API Testing
Run the comprehensive test suite:
```bash
poetry run python test_api.py
```

This will test all endpoints and demonstrate the full functionality.

### Manual Testing
Use the interactive API documentation at `/docs` to test endpoints manually.

### Unit Tests
Run the test suite:
```bash
poetry run pytest
```

## 📊 Usage Examples

### Creating a Firewall Device
```python
import requests
import uuid

device_data = {
    "name": "Firewall-DMZ-01",
    "hostname": "fw-dmz-01.company.com", 
    "version": "9.1.5",
    "brand": "Palo Alto",
    "model": "PA-3220",
    "serial_number": "001234567890",
    "location": "Data Center - DMZ",
    "user_id": str(uuid.uuid4()),
    "is_active": True
}

response = requests.post("http://localhost:8000/api/v1/devices/", json=device_data)
print(response.json())
```

### Searching Devices by Version
```python
response = requests.get("http://localhost:8000/api/v1/devices/search/by-version?version=9.1.5")
devices = response.json()
```

### Getting Version Summary
```python
response = requests.get("http://localhost:8000/api/v1/devices/versions/summary")
summary = response.json()
```

## 🏗️ Project Structure

```
vulntrack-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/v1/              # API version 1
│   │   ├── api.py           # API router configuration
│   │   └── endpoints/       # API endpoints
│   │       └── devices.py   # Device management endpoints
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   │   └── device.py        # Device data model
│   ├── schemas/             # Pydantic schemas
│   │   └── device.py        # Device validation schemas
│   └── services/            # Business logic
│       └── device_service.py # Device management service
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── init_db.py              # Database initialization
├── test_api.py             # API testing script
└── pyproject.toml          # Project configuration
```

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - ORM with declarative base
- **PostgreSQL** - Primary database
- **Pydantic v2** - Data validation and serialization
- **Alembic** - Database migrations
- **Poetry** - Dependency management
- **Uvicorn** - ASGI server

## 🔧 Configuration

The application uses environment-based configuration. Key settings:

- `APP_PORT`: Application port (default: 8000)
- `ENVIRONMENT`: Runtime environment (development/production)
- `DB_*`: Database connection parameters
- `DATABASE_URL`: Complete database connection string

## 🗄️ Database Schema

### Devices Table
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

### Indexes
- Primary key on `id`
- Unique indexes on `hostname`, `serial_number`
- Performance indexes on `name`, `user_id`

## 🚦 API Response Examples

### Device Creation Response
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Firewall-DMZ-01",
    "hostname": "fw-dmz-01.company.com",
    "version": "9.1.5",
    "brand": "Palo Alto", 
    "model": "PA-3220",
    "serial_number": "001234567890",
    "location": "Data Center - DMZ",
    "user_id": "987fcdeb-51d2-43e8-9012-345678901234",
    "is_active": true,
    "created_at": "2025-06-11T10:30:00Z",
    "updated_at": "2025-06-11T10:30:00Z"
}
```

### Device List Response
```json
{
    "devices": [...],
    "total": 42,
    "page": 1,
    "size": 10,
    "pages": 5
}
```

## 🔮 Future Enhancements

- **Vulnerability Scanning** integration
- **Compliance Reporting** features  
- **Device Grouping** and tagging
- **Automated Discovery** capabilities
- **Integration APIs** for monitoring tools
- **Audit Logging** for all changes
- **Role-based Access Control**
- **Device Configuration** backup/restore

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