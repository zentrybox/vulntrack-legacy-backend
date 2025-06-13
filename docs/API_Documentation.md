# VulnTrack API Documentation & Testing Collections

This directory contains comprehensive API documentation and testing collections for the VulnTrack vulnerability scanning backend.

## 📁 Files Overview

- **`Insomnia_sample_doc_endpoint.yaml`** - Complete Insomnia REST Client collection
- **`VulnTrack_Postman_Collection.json`** - Complete Postman collection
- **`API_Documentation.md`** - This comprehensive API documentation

## 🚀 Quick Start

### 1. Start the VulnTrack Backend
```bash
cd vulntrack-legacy-backend
uvicorn app.main:app --port 8000 --reload
```

### 2. Import Collections

**For Insomnia:**
1. Open Insomnia
2. Go to Application → Preferences → Data → Import Data
3. Select `Insomnia_sample_doc_endpoint.yaml`
4. Update environment variables as needed

**For Postman:**
1. Open Postman
2. Click Import → Upload Files
3. Select `VulnTrack_Postman_Collection.json`
4. Update collection variables as needed

## 🔧 Environment Variables

Set these variables in your testing client:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://127.0.0.1:8000` | Backend server URL |
| `sample_device_id` | `12345678-1234-1234-1234-123456789abc` | Sample device UUID |
| `sample_device_id_2` | `87654321-4321-4321-4321-cba987654321` | Second sample device UUID |
| `brave_api_key` | `YOUR_BRAVE_API_KEY` | Your Brave Search API key |

## 📊 API Endpoints Overview

### System Status
- **GET** `/` - Health check / Welcome message
- **GET** `/api/v1/vulnerabilities/scan/status` - Vulnerability scanning system status

### Device Management
- **GET** `/api/v1/devices/` - List all devices
- **POST** `/api/v1/devices/` - Create new device
- **GET** `/api/v1/devices/{device_id}` - Get device by ID
- **PUT** `/api/v1/devices/{device_id}` - Update device
- **DELETE** `/api/v1/devices/{device_id}` - Delete device

### Vulnerability Scanning
- **POST** `/api/v1/vulnerabilities/scan/device/{device_id}` - Full vulnerability scan
- **POST** `/api/v1/vulnerabilities/scan/device/{device_id}/local` - Local CVE database only
- **POST** `/api/v1/vulnerabilities/scan/device/{device_id}/ai` - AI knowledge only
- **POST** `/api/v1/vulnerabilities/scan/device/{device_id}/web` - Web search + AI filtering
- **POST** `/api/v1/vulnerabilities/scan/device/{device_id}/quick` - Quick check (alias for local)
- **POST** `/api/v1/vulnerabilities/scan/devices/batch` - Batch device scanning

## 🔍 Vulnerability Scanning Methods

### 1. **Full Scan** (`/scan/device/{device_id}`)
- **Process**: Local CVE DB → Web Search → AI Analysis
- **Speed**: Slowest but most comprehensive
- **Cost**: Uses API quotas (Brave Search + Gemini AI)
- **Use Case**: Comprehensive security assessment

### 2. **Local Scan Only** (`/scan/device/{device_id}/local`)
- **Process**: MongoDB CVE database only
- **Speed**: Fastest
- **Cost**: Free (no external APIs)
- **Use Case**: Quick checks, cost-sensitive environments

### 3. **AI Knowledge Only** (`/scan/device/{device_id}/ai`)
- **Process**: Gemini AI built-in knowledge
- **Speed**: Fast
- **Cost**: Gemini AI quota only
- **Use Case**: Leverage AI knowledge without web searches

### 4. **Web Search + AI** (`/scan/device/{device_id}/web`)
- **Process**: Brave Search → AI filtering
- **Speed**: Medium
- **Cost**: Both Brave Search + Gemini AI quotas
- **Use Case**: Most recent vulnerability information

### 5. **Quick Check** (`/scan/device/{device_id}/quick`)
- **Process**: Alias for local scan
- **Speed**: Fastest
- **Cost**: Free
- **Use Case**: Rapid vulnerability assessment

### 6. **Batch Scanning** (`/scan/devices/batch`)
- **Process**: Multiple devices, optimized for bulk operations
- **Speed**: Optimized bulk processing
- **Cost**: Varies based on scan results
- **Use Case**: Infrastructure-wide vulnerability assessment

## 📝 Sample Requests

### Create Device
```json
POST /api/v1/devices/
{
  "hostname": "firewall-01.company.com",
  "ip_address": "192.168.1.100",
  "brand": "Palo Alto Networks",
  "model": "PA-220",
  "version": "9.1.3",
  "device_type": "firewall",
  "location": "Main Office",
  "is_active": true
}
```

### Batch Scan Request
```json
POST /api/v1/vulnerabilities/scan/devices/batch
[
  "12345678-1234-1234-1234-123456789abc",
  "87654321-4321-4321-4321-cba987654321"
]
```

## 📊 Response Examples

### Successful Vulnerability Scan
```json
{
  "success": true,
  "message": "Vulnerability scan completed",
  "source": "web_search_ai_filtered",
  "device_info": {
    "id": "12345678-1234-1234-1234-123456789abc",
    "hostname": "firewall-01.company.com",
    "brand": "Palo Alto Networks",
    "model": "PA-220",
    "version": "9.1.3"
  },
  "vulnerabilities_found": true,
  "vulnerability_count": 2,
  "vulnerabilities": [
    {
      "cve_id": "CVE-2023-12345",
      "severity": "High",
      "description": "Authentication bypass vulnerability",
      "cvss_score": "8.1"
    }
  ],
  "confidence_score": 0.95,
  "scan_timestamp": "2025-06-13T10:30:00Z"
}
```

### System Status Response
```json
{
  "vulnerability_scanning": {
    "enabled": true,
    "configuration": {
      "batch_size": 5,
      "timeout": 30,
      "max_retries": 3,
      "rate_limit_delay": 1.0,
      "cache_ttl": 3600
    },
    "apis": {
      "gemini_model": "gemini-1.5-flash",
      "gemini_configured": true,
      "brave_search_configured": true,
      "mongodb_configured": true
    }
  }
}
```

## 🔧 External API Testing

The collections include direct external API testing endpoints:

### Brave Search API (Clean Parameters)
- **URL**: `https://api.search.brave.com/res/v1/web/search`
- **Parameters**: `q`, `count`, `freshness`, `result_filter`
- **Note**: Language and country parameters removed to avoid validation errors

### Example Queries:
- Palo Alto Networks PA-220 9.1.3 vulnerability CVE security exploit
- Cisco ASA 5505 8.2.5 vulnerability CVE security exploit

## 🚨 Important Notes

### API Keys Required
1. **Brave Search API Key** - Set in environment variable `BRAVE_SEARCH_API_KEY`
2. **Gemini AI API Key** - Set in environment variable `GEMINI_API_KEY`

### Rate Limits
- Brave Search: Depends on your subscription plan
- Gemini AI: Depends on your quota
- Local MongoDB: No limits

### Error Handling
All endpoints include comprehensive error handling:
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (device doesn't exist)
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

## 🔍 Testing Workflow

### 1. Basic Health Check
1. Test `GET /` endpoint
2. Test `GET /api/v1/vulnerabilities/scan/status`

### 2. Device Management
1. Create a test device with `POST /api/v1/devices/`
2. List devices with `GET /api/v1/devices/`
3. Get specific device details
4. Update device information
5. Delete test device (cleanup)

### 3. Vulnerability Scanning
1. Start with local scan (fastest, free)
2. Test AI-only scan
3. Test web search + AI scan
4. Test full comprehensive scan
5. Test batch scanning with multiple devices

### 4. External API Validation
1. Test Brave Search API directly
2. Verify clean parameters work without validation errors
3. Test different device queries

## 📈 Performance Testing

Use the collections to test:
- Response times for different scan types
- API quota consumption
- Error handling under load
- Batch processing efficiency

## 🛠️ Customization

### Adding New Test Cases
1. Duplicate existing requests
2. Modify device parameters (brand, model, version)
3. Test with different vulnerability scenarios

### Environment Switching
Update environment variables to test:
- Local development (`http://127.0.0.1:8000`)
- Staging environment
- Production environment

## 📞 Support

For issues with the API collections or documentation:
1. Check server logs for detailed error information
2. Verify all environment variables are set correctly
3. Ensure external API keys are valid and have sufficient quota
4. Review the main project README for setup instructions
