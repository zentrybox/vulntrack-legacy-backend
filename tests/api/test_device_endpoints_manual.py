#!/usr/bin/env python3
"""
Test script for the Device Management API
This script demonstrates how to interact with the firewall device management endpoints.
"""

import requests
import json
import uuid
from datetime import datetime

# API base URL
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_health_check():
    """Test the basic health endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_device():
    """Test creating a new device"""
    print("=== Testing Device Creation ===")
    
    # Generate a unique user ID for testing
    user_id = str(uuid.uuid4())
    
    device_data = {
        "name": "Firewall-Main-001",
        "hostname": "fw-main-001.company.local",
        "version": "9.1.0",
        "brand": "Palo Alto",
        "model": "PA-3220",
        "serial_number": "PA3220-001-2024",
        "location": "Data Center - Rack A1",
        "user_id": user_id,
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/devices/", json=device_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        device = response.json()
        print(f"Created device: {device['name']} (ID: {device['id']})")
        return device
    else:
        print(f"Error: {response.json()}")
        return None

def test_get_devices():
    """Test retrieving all devices"""
    print("=== Testing Get All Devices ===")
    
    response = requests.get(f"{BASE_URL}/devices/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total devices: {data['total']}")
        print(f"Current page: {data['page']}")
        print(f"Devices on this page: {data['size']}")
        
        for device in data['devices']:
            print(f"  - {device['name']} ({device['brand']} {device['model']}) - Version: {device['version']}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_search_by_version():
    """Test searching devices by version"""
    print("=== Testing Search by Version ===")
    
    response = requests.get(f"{BASE_URL}/devices/search/by-version?version=9.1.0")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        devices = response.json()
        print(f"Found {len(devices)} devices with version 9.1.0:")
        for device in devices:
            print(f"  - {device['name']} ({device['hostname']})")
    else:
        print(f"Error: {response.json()}")
    print()

def test_version_summary():
    """Test getting version summary"""
    print("=== Testing Version Summary ===")
    
    response = requests.get(f"{BASE_URL}/devices/versions/summary")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Version Summary:")
        for item in data['version_summary']:
            print(f"  - {item['brand']} {item['version']}: {item['device_count']} devices")
    else:
        print(f"Error: {response.json()}")
    print()

def test_general_search():
    """Test general search functionality"""
    print("=== Testing General Search ===")
    
    response = requests.get(f"{BASE_URL}/devices/search/general?q=Palo")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        devices = response.json()
        print(f"Found {len(devices)} devices matching 'Palo':")
        for device in devices:
            print(f"  - {device['name']} ({device['brand']} {device['model']})")
    else:
        print(f"Error: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("Device Management API Test Suite")
    print("=" * 50)
    print()
    
    try:
        # Test basic health
        test_health_check()
        
        # Test device creation
        device = test_create_device()
        print()
        
        # Test retrieving devices
        test_get_devices()
        
        # Test search functionality
        test_search_by_version()
        test_version_summary()
        test_general_search()
        
        print("=" * 50)
        print("All tests completed!")
        print("You can now:")
        print("1. Visit http://127.0.0.1:8000/docs for the interactive API documentation")
        print("2. Visit http://127.0.0.1:8000/redoc for alternative documentation")
        print("3. Use the API endpoints to manage your firewall devices")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Make sure the server is running with: poetry run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
