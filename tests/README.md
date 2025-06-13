# VulnTrack Tests

This directory contains all tests and demo scripts for the VulnTrack backend project.

## Directory Structure

```
tests/
├── __init__.py                           # Main tests package
├── README.md                            # This file
├── unit/                                # Unit tests
│   ├── __init__.py
│   └── test_app_endpoints.py           # Tests for main FastAPI app endpoints
├── api/                                 # API endpoint tests
│   ├── __init__.py
│   ├── test_device_endpoints_manual.py # Manual device API endpoint tests
│   └── test_device_workflow_integration.py # Device workflow integration tests
└── demos/                               # Demo and example scripts
    ├── __init__.py
    └── comprehensive_api_showcase.py    # Complete API feature demonstration
```

## Test Categories

### Unit Tests (`unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Framework**: pytest with FastAPI TestClient
- **Files**:
  - `test_app_endpoints.py`: Tests for main application endpoints and health checks

### API Tests (`api/`)
- **Purpose**: Test API endpoints with actual HTTP requests
- **Framework**: requests library for live API testing
- **Files**:
  - `test_device_endpoints_manual.py`: Manual testing script for device management endpoints
  - `test_device_workflow_integration.py`: Integration tests for complete device workflows

### Demos (`demos/`)
- **Purpose**: Demonstration scripts and usage examples
- **Use Case**: Show how to use the API, provide examples for integration
- **Files**:
  - `comprehensive_api_showcase.py`: Complete demonstration of all device management features

## Running Tests

### Prerequisites
Make sure the FastAPI server is running:
```bash
poetry run uvicorn app.main:app --reload
```

### Unit Tests
```bash
# Run all unit tests
poetry run pytest tests/unit/

# Run specific unit test
poetry run pytest tests/unit/test_app_endpoints.py -v
```

### API Tests
```bash
# Run API tests (requires running server)
python tests/api/test_device_endpoints_manual.py
python tests/api/test_device_workflow_integration.py
```

### Demo Scripts
```bash
# Run comprehensive demo
python tests/demos/comprehensive_api_showcase.py
```

## Test Data

Tests use sample device data with the following structure:
- **Brands**: Palo Alto, Fortinet, Cisco
- **Models**: PA-3220, FortiGate-200E, ASA-5506-X
- **Locations**: DMZ Network, Internal Network, Branch Office
- **Random UUIDs**: Generated for user_id fields

## Adding New Tests

### Unit Tests
- Add new test files to `tests/unit/`
- Use pytest conventions (`test_*.py` files, `test_*` functions)
- Import from `app.*` modules
- Use FastAPI TestClient for endpoint testing

### API Tests
- Add new test files to `tests/api/`
- Use requests library for HTTP calls
- Test against live server on localhost:8000
- Include proper error handling and assertions

### Demo Scripts
- Add new demo files to `tests/demos/`
- Focus on demonstrating real-world usage
- Include comprehensive examples and output formatting
- Add helpful comments and documentation

## Notes

- All test files should include proper docstrings
- API tests require the server to be running
- Use meaningful test data that reflects real-world scenarios
- Follow naming conventions for easy identification
