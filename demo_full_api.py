#!/usr/bin/env python3
"""
Extended test script demonstrating all Device Management API features
"""

import requests
import json
import uuid
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/v1"

def create_sample_devices():
    """Create several sample devices for testing"""
    print("=== Creating Sample Devices ===")
    
    devices = [
        {
            "name": "Firewall-DMZ-001",
            "hostname": "fw-dmz-001.company.local",
            "version": "9.0.5",
            "brand": "Palo Alto",
            "model": "PA-3220",
            "serial_number": "PA3220-DMZ-001",
            "location": "DMZ Network",
            "user_id": str(uuid.uuid4()),
            "is_active": True
        },
        {
            "name": "Firewall-LAN-001", 
            "hostname": "fw-lan-001.company.local",
            "version": "9.1.0",
            "brand": "Fortinet",
            "model": "FortiGate-200E",
            "serial_number": "FG200E-LAN-001",
            "location": "Internal Network",
            "user_id": str(uuid.uuid4()),
            "is_active": True
        },
        {
            "name": "Firewall-Branch-001",
            "hostname": "fw-branch-001.company.local", 
            "version": "8.5.2",
            "brand": "Cisco",
            "model": "ASA-5506-X",
            "serial_number": "ASA5506-BR-001",
            "location": "Branch Office",
            "user_id": str(uuid.uuid4()),
            "is_active": False
        }
    ]
    
    created_devices = []
    for device_data in devices:
        response = requests.post(f"{BASE_URL}/devices/", json=device_data)
        if response.status_code == 201:
            device = response.json()
            print(f"✓ Created: {device['name']} ({device['brand']} {device['model']})")
            created_devices.append(device)
        else:
            print(f"✗ Failed to create {device_data['name']}: {response.text}")
    
    print(f"Created {len(created_devices)} devices")
    print()
    return created_devices

def test_device_search():
    """Test various search capabilities"""
    print("=== Testing Device Search Capabilities ===")
    
    # Search by brand
    print("🔍 Search by brand 'Palo':")
    response = requests.get(f"{BASE_URL}/devices/search/by-brand?brand=Palo")
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            print(f"  - {device['name']} ({device['brand']} {device['model']})")
    
    # Search by version
    print("\n🔍 Search by version '9.1.0':")
    response = requests.get(f"{BASE_URL}/devices/search/by-version?version=9.1.0")
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            print(f"  - {device['name']} - {device['version']}")
    
    # General search
    print("\n🔍 General search for 'DMZ':")
    response = requests.get(f"{BASE_URL}/devices/search/general?q=DMZ")
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            print(f"  - {device['name']} at {device['location']}")
    print()

def test_device_filtering():
    """Test device filtering options"""
    print("=== Testing Device Filtering ===")
    
    # Filter active devices
    print("📊 Active devices only:")
    response = requests.get(f"{BASE_URL}/devices/?is_active=true")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total']} active devices:")
        for device in data['devices']:
            print(f"  - {device['name']} ({'Active' if device['is_active'] else 'Inactive'})")
    
    # Filter inactive devices
    print("\n📊 Inactive devices only:")
    response = requests.get(f"{BASE_URL}/devices/?is_active=false")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total']} inactive devices:")
        for device in data['devices']:
            print(f"  - {device['name']} ({'Active' if device['is_active'] else 'Inactive'})")
    print()

def test_device_update():
    """Test device update functionality"""
    print("=== Testing Device Update ===")
    
    # Get first device
    response = requests.get(f"{BASE_URL}/devices/?limit=1")
    if response.status_code == 200:
        devices = response.json()['devices']
        if devices:
            device = devices[0]
            device_id = device['id']
            
            print(f"Updating device: {device['name']}")
            print(f"Current version: {device['version']}")
            
            # Update version
            update_data = {
                "version": "9.2.0",
                "location": "Updated Location - " + device['location']
            }
            
            response = requests.put(f"{BASE_URL}/devices/{device_id}", json=update_data)
            if response.status_code == 200:
                updated_device = response.json()
                print(f"✓ Updated version: {updated_device['version']}")
                print(f"✓ Updated location: {updated_device['location']}")
            else:
                print(f"✗ Update failed: {response.text}")
    print()

def test_version_analysis():
    """Test version analysis features"""
    print("=== Testing Version Analysis ===")
    
    # Version summary
    print("📈 Version Summary:")
    response = requests.get(f"{BASE_URL}/devices/versions/summary")
    if response.status_code == 200:
        data = response.json()
        for item in data['version_summary']:
            print(f"  - {item['brand']} {item['version']}: {item['device_count']} device(s)")
    
    # Detailed version list
    print("\n📋 Detailed Version Information:")
    response = requests.get(f"{BASE_URL}/devices/versions/list")
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            print(f"  - {device['device_name']}: {device['brand']} {device['current_version']}")
            print(f"    Location: {device['location']}, Host: {device['hostname']}")
    print()

def test_device_deactivation():
    """Test device deactivation (soft delete)"""
    print("=== Testing Device Deactivation ===")
    
    # Find an active device
    response = requests.get(f"{BASE_URL}/devices/?is_active=true&limit=1")
    if response.status_code == 200:
        devices = response.json()['devices']
        if devices:
            device = devices[0]
            device_id = device['id']
            
            print(f"Deactivating device: {device['name']}")
            
            response = requests.patch(f"{BASE_URL}/devices/{device_id}/deactivate")
            if response.status_code == 200:
                deactivated_device = response.json()
                print(f"✓ Device deactivated: {deactivated_device['name']}")
                print(f"  Status: {'Active' if deactivated_device['is_active'] else 'Inactive'}")
            else:
                print(f"✗ Deactivation failed: {response.text}")
    print()

def main():
    """Run comprehensive API demonstration"""
    print("🔥 Comprehensive Device Management API Demo")
    print("=" * 60)
    print()
    
    try:
        # Create sample devices
        created_devices = create_sample_devices()
        
        # Test search capabilities
        test_device_search()
        
        # Test filtering
        test_device_filtering()
        
        # Test updates
        test_device_update()
        
        # Test version analysis
        test_version_analysis()
        
        # Test deactivation
        test_device_deactivation()
        
        print("=" * 60)
        print("🎉 Comprehensive demo completed successfully!")
        print()
        print("Key Features Demonstrated:")
        print("✅ Device Creation (CRUD)")
        print("✅ Device Search & Filtering")
        print("✅ Version Management")
        print("✅ Device Updates")
        print("✅ Device Deactivation")
        print("✅ Analytics & Reporting")
        print()
        print("Next Steps:")
        print("1. Visit http://127.0.0.1:8000/docs for interactive API docs")
        print("2. Integrate with your monitoring tools")
        print("3. Set up automated device discovery")
        print("4. Configure vulnerability scanning")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API server.")
        print("Make sure the server is running with:")
        print("poetry run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
