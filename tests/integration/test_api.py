"""
Test script to demonstrate the Device Management API
This script shows how to use all the device management endpoints
"""
import uuid
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_device_api():
    """Test all device management endpoints"""
    
    # Sample device data for testing
    test_device = {
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
    
    print("🔥 Testing Device Management API")
    print("=" * 50)
    
    # Test 1: Create a device
    print("\n1. Creating a new firewall device...")
    response = requests.post(f"{BASE_URL}/devices/", json=test_device)
    if response.status_code == 201:
        device = response.json()
        device_id = device["id"]
        print(f"✅ Device created successfully! ID: {device_id}")
        print(f"   Name: {device['name']}")
        print(f"   Hostname: {device['hostname']}")
        print(f"   Version: {device['version']}")
    else:
        print(f"❌ Failed to create device: {response.status_code}")
        print(response.text)
        return
    
    # Test 2: Get the device by ID
    print(f"\n2. Retrieving device by ID: {device_id}")
    response = requests.get(f"{BASE_URL}/devices/{device_id}")
    if response.status_code == 200:
        device = response.json()
        print(f"✅ Device retrieved successfully!")
        print(f"   Name: {device['name']}")
        print(f"   Brand: {device['brand']} {device['model']}")
    else:
        print(f"❌ Failed to retrieve device: {response.status_code}")
    
    # Test 3: Update device version (simulating firmware update)
    print(f"\n3. Updating device version (firmware update)...")
    update_data = {"version": "9.1.6"}
    response = requests.put(f"{BASE_URL}/devices/{device_id}", json=update_data)
    if response.status_code == 200:
        updated_device = response.json()
        print(f"✅ Device updated successfully!")
        print(f"   Old version: 9.1.5")
        print(f"   New version: {updated_device['version']}")
    else:
        print(f"❌ Failed to update device: {response.status_code}")
    
    # Test 4: Create another device for testing search
    test_device2 = {
        "name": "Firewall-WAN-01", 
        "hostname": "fw-wan-01.company.com",
        "version": "9.1.4",
        "brand": "Palo Alto",
        "model": "PA-5220",
        "serial_number": "001234567891", 
        "location": "Data Center - WAN",
        "user_id": str(uuid.uuid4()),
        "is_active": True
    }
    
    print(f"\n4. Creating second device for testing...")
    response = requests.post(f"{BASE_URL}/devices/", json=test_device2)
    if response.status_code == 201:
        device2 = response.json()
        device2_id = device2["id"]
        print(f"✅ Second device created! ID: {device2_id}")
    else:
        print(f"❌ Failed to create second device: {response.status_code}")
        return
    
    # Test 5: List all devices
    print(f"\n5. Listing all devices...")
    response = requests.get(f"{BASE_URL}/devices/")
    if response.status_code == 200:
        devices_list = response.json()
        print(f"✅ Retrieved {devices_list['total']} devices:")
        for device in devices_list['devices']:
            print(f"   - {device['name']} ({device['hostname']}) - v{device['version']}")
    else:
        print(f"❌ Failed to list devices: {response.status_code}")
    
    # Test 6: Search devices by brand
    print(f"\n6. Searching devices by brand 'Palo Alto'...")
    response = requests.get(f"{BASE_URL}/devices/search/by-brand?brand=Palo Alto")
    if response.status_code == 200:
        devices = response.json()
        print(f"✅ Found {len(devices)} Palo Alto devices:")
        for device in devices:
            print(f"   - {device['name']} ({device['model']}) - v{device['version']}")
    else:
        print(f"❌ Failed to search devices: {response.status_code}")
    
    # Test 7: Get version summary
    print(f"\n7. Getting version summary...")
    response = requests.get(f"{BASE_URL}/devices/versions/summary")
    if response.status_code == 200:
        summary = response.json()
        print(f"✅ Version summary:")
        for item in summary['version_summary']:
            print(f"   - {item['brand']} v{item['version']}: {item['device_count']} device(s)")
    else:
        print(f"❌ Failed to get version summary: {response.status_code}")
    
    # Test 8: Search devices by name
    print(f"\n8. Searching devices by name 'Firewall'...")
    response = requests.get(f"{BASE_URL}/devices/search/by-name?name=Firewall")
    if response.status_code == 200:
        devices = response.json()
        print(f"✅ Found {len(devices)} devices with 'Firewall' in name:")
        for device in devices:
            print(f"   - {device['name']} at {device['location']}")
    else:
        print(f"❌ Failed to search by name: {response.status_code}")
    
    # Test 9: Deactivate a device (soft delete)
    print(f"\n9. Deactivating device {device2_id}...")
    response = requests.patch(f"{BASE_URL}/devices/{device2_id}/deactivate")
    if response.status_code == 200:
        deactivated_device = response.json()
        print(f"✅ Device deactivated successfully!")
        print(f"   Active status: {deactivated_device['is_active']}")
    else:
        print(f"❌ Failed to deactivate device: {response.status_code}")
    
    # Test 10: List only active devices
    print(f"\n10. Listing only active devices...")
    response = requests.get(f"{BASE_URL}/devices/?is_active=true")
    if response.status_code == 200:
        devices_list = response.json()
        print(f"✅ Active devices: {devices_list['total']}")
        for device in devices_list['devices']:
            print(f"   - {device['name']} (Active: {device['is_active']})")
    else:
        print(f"❌ Failed to list active devices: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 Device Management API testing completed!")
    print("\nThe API provides the following features:")
    print("✅ Create, Read, Update, Delete devices")
    print("✅ Search devices by name, brand, version")
    print("✅ Version management and tracking")
    print("✅ Device activation/deactivation")
    print("✅ Pagination and filtering")
    print("✅ Comprehensive device information management")

if __name__ == "__main__":
    try:
        test_device_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("Please make sure the FastAPI server is running on http://localhost:8000")
        print("Run: poetry run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
