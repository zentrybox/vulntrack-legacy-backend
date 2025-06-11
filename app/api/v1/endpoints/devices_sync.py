import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    DeviceList,
    DeviceVersionInfo
)
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
):
    """Create a new firewall device"""
    service = DeviceService(db)
    
    # Check if hostname already exists
    existing_device = service.get_device_by_hostname(device_data.hostname)
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device with hostname '{device_data.hostname}' already exists"
        )
    
    # Check if serial number already exists
    existing_device = service.get_device_by_serial_number(device_data.serial_number)
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device with serial number '{device_data.serial_number}' already exists"
        )
    
    try:
        device = service.create_device(device_data)
        return device
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create device: {str(e)}"
        )


@router.get("/", response_model=DeviceList)
def get_devices(
    skip: int = Query(0, ge=0, description="Number of devices to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of devices to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    user_id: Optional[uuid.UUID] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get all devices with pagination and filtering"""
    service = DeviceService(db)
    
    devices = service.get_devices(skip=skip, limit=limit, is_active=is_active, user_id=user_id)
    total = service.get_device_count(is_active=is_active)
    
    return DeviceList(
        devices=devices,
        total=total,
        page=skip // limit + 1,
        size=len(devices),
        pages=(total + limit - 1) // limit
    )


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get a specific device by ID"""
    service = DeviceService(db)
    device = service.get_device_by_id(device_id)
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: uuid.UUID,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """Update a device"""
    service = DeviceService(db)
    
    # Check if device exists
    existing_device = service.get_device_by_id(device_id)
    if not existing_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    
    # Check for hostname conflicts if hostname is being updated
    if device_data.hostname and device_data.hostname != existing_device.hostname:
        hostname_conflict = service.get_device_by_hostname(device_data.hostname)
        if hostname_conflict and hostname_conflict.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device with hostname '{device_data.hostname}' already exists"
            )
    
    # Check for serial number conflicts if serial number is being updated
    if device_data.serial_number and device_data.serial_number != existing_device.serial_number:
        serial_conflict = service.get_device_by_serial_number(device_data.serial_number)
        if serial_conflict and serial_conflict.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device with serial number '{device_data.serial_number}' already exists"
            )
    
    try:
        updated_device = service.update_device(device_id, device_data)
        return updated_device
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update device: {str(e)}"
        )


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Delete a device permanently"""
    service = DeviceService(db)
    
    success = service.delete_device(device_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )


@router.patch("/{device_id}/deactivate", response_model=DeviceResponse)
def deactivate_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Deactivate a device (soft delete)"""
    service = DeviceService(db)
    
    device = service.deactivate_device(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    
    return device


@router.get("/search/by-name", response_model=List[DeviceResponse])
def get_devices_by_name(
    name: str = Query(..., min_length=1, description="Device name to search for"),
    db: Session = Depends(get_db)
):
    """Get devices by name (partial match)"""
    service = DeviceService(db)
    devices = service.get_devices_by_name(name)
    return devices


@router.get("/search/by-version", response_model=List[DeviceResponse])
def get_devices_by_version(
    version: str = Query(..., min_length=1, description="Version to search for"),
    db: Session = Depends(get_db)
):
    """Get devices by specific version"""
    service = DeviceService(db)
    devices = service.get_devices_by_version(version)
    return devices


@router.get("/search/by-brand", response_model=List[DeviceResponse])
def get_devices_by_brand(
    brand: str = Query(..., min_length=1, description="Brand to search for"),
    model: Optional[str] = Query(None, description="Optional model to filter by"),
    db: Session = Depends(get_db)
):
    """Get devices by brand and optionally by model"""
    service = DeviceService(db)
    devices = service.get_devices_by_brand_and_model(brand, model)
    return devices


@router.get("/search/general", response_model=List[DeviceResponse])
def search_devices(
    q: str = Query(..., min_length=1, description="Search term"),
    db: Session = Depends(get_db)
):
    """Search devices by name, hostname, brand, model, location, or serial number"""
    service = DeviceService(db)
    devices = service.search_devices(q)
    return devices


@router.get("/versions/summary")
def get_version_summary(
    db: Session = Depends(get_db)
):
    """Get version summary for all active devices"""
    service = DeviceService(db)
    summary = service.get_version_summary()
    return {"version_summary": summary}


@router.get("/versions/list", response_model=List[DeviceVersionInfo])
def get_devices_version_info(
    db: Session = Depends(get_db)
):
    """Get version information for all active devices"""
    service = DeviceService(db)
    devices = service.get_devices(is_active=True)
    
    version_info = []
    for device in devices:
        version_info.append(DeviceVersionInfo(
            device_id=device.id,
            device_name=device.name,
            current_version=device.version,
            brand=device.brand,
            model=device.model,
            hostname=device.hostname,
            location=device.location,
            is_active=device.is_active,
            last_updated=device.updated_at
        ))
    
    return version_info
