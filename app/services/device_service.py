import uuid
from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def create_device(self, device_data: DeviceCreate) -> Device:
        """Create a new device"""
        device = Device(**device_data.model_dump())
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def get_device_by_id(self, device_id: uuid.UUID) -> Optional[Device]:
        """Get a device by ID"""
        return self.db.query(Device).filter(Device.id == device_id).first()

    def get_device_by_hostname(self, hostname: str) -> Optional[Device]:
        """Get a device by hostname"""
        return self.db.query(Device).filter(Device.hostname == hostname.lower()).first()

    def get_device_by_serial_number(self, serial_number: str) -> Optional[Device]:
        """Get a device by serial number"""
        return (
            self.db.query(Device)
            .filter(Device.serial_number == serial_number.upper())
            .first()
        )

    def get_devices(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        user_id: Optional[uuid.UUID] = None,
    ) -> List[Device]:
        """Get all devices with optional filtering"""
        query = self.db.query(Device)

        # Apply filters
        if is_active is not None:
            query = query.filter(Device.is_active == is_active)
        if user_id is not None:
            query = query.filter(Device.user_id == user_id)

        return query.order_by(Device.created_at.desc()).offset(skip).limit(limit).all()

    def get_devices_by_name(self, name: str) -> List[Device]:
        """Get devices by name (partial match)"""
        return (
            self.db.query(Device)
            .filter(Device.name.ilike(f"%{name}%"))
            .order_by(Device.name)
            .all()
        )

    def get_devices_by_version(self, version: str) -> List[Device]:
        """Get devices by version"""
        return (
            self.db.query(Device)
            .filter(Device.version == version)
            .order_by(Device.name)
            .all()
        )

    def get_devices_by_brand_and_model(
        self, brand: str, model: Optional[str] = None
    ) -> List[Device]:
        """Get devices by brand and optionally by model"""
        query = self.db.query(Device).filter(Device.brand.ilike(f"%{brand}%"))

        if model:
            query = query.filter(Device.model.ilike(f"%{model}%"))

        return query.order_by(Device.brand, Device.model, Device.name).all()

    def update_device(
        self, device_id: uuid.UUID, device_data: DeviceUpdate
    ) -> Optional[Device]:
        """Update a device"""
        device = self.get_device_by_id(device_id)
        if not device:
            return None

        update_data = device_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)

        self.db.commit()
        self.db.refresh(device)
        return device

    def delete_device(self, device_id: uuid.UUID) -> bool:
        """Delete a device"""
        device = self.get_device_by_id(device_id)
        if not device:
            return False

        self.db.delete(device)
        self.db.commit()
        return True

    def deactivate_device(self, device_id: uuid.UUID) -> Optional[Device]:
        """Deactivate a device (soft delete)"""
        device = self.get_device_by_id(device_id)
        if not device:
            return None

        device.is_active = False
        self.db.commit()
        self.db.refresh(device)
        return device

    def get_device_count(self, is_active: Optional[bool] = None) -> int:
        """Get total count of devices"""
        query = self.db.query(Device)

        if is_active is not None:
            query = query.filter(Device.is_active == is_active)

        return query.count()

    def get_version_summary(self) -> List[dict[str, object]]:
        """Get version summary for all active devices"""
        result = (
            self.db.query(
                Device.version,
                Device.brand,
                func.count(Device.id).label("device_count"),
            )
            .filter(Device.is_active == True)  # noqa: E712
            .group_by(Device.version, Device.brand)
            .order_by(Device.brand, Device.version)
            .all()
        )

        return [
            {
                "version": row.version,
                "brand": row.brand,
                "device_count": row.device_count,
            }
            for row in result
        ]

    def search_devices(self, search_term: str) -> List[Device]:
        """Search devices by name, hostname, brand, model, or location"""
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(Device)
            .filter(
                or_(
                    Device.name.ilike(search_pattern),
                    Device.hostname.ilike(search_pattern),
                    Device.brand.ilike(search_pattern),
                    Device.model.ilike(search_pattern),
                    Device.location.ilike(search_pattern),
                    Device.serial_number.ilike(search_pattern),
                )
            )
            .order_by(Device.name)
            .all()
        )
