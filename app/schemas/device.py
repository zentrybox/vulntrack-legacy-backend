import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Device name")
    hostname: str = Field(
        ..., min_length=1, max_length=255, description="Device hostname"
    )
    version: str = Field(
        ..., min_length=1, max_length=100, description="Firmware/Software version"
    )
    brand: str = Field(..., min_length=1, max_length=100, description="Device brand")
    model: str = Field(..., min_length=1, max_length=100, description="Device model")
    serial_number: str = Field(
        ..., min_length=1, max_length=100, description="Device serial number"
    )
    location: str = Field(
        ..., min_length=1, max_length=255, description="Device location"
    )
    user_id: uuid.UUID = Field(
        ..., description="ID of the user responsible for this device"
    )
    is_active: bool = Field(default=True, description="Whether the device is active")

    @field_validator("hostname")
    @classmethod
    def validate_hostname(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Hostname cannot be empty")
        return v.strip().lower()

    @field_validator("serial_number")
    @classmethod
    def validate_serial_number(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Serial number cannot be empty")
        return v.strip().upper()


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    hostname: Optional[str] = Field(None, min_length=1, max_length=255)
    version: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    user_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None

    @field_validator("hostname")
    @classmethod
    def validate_hostname(cls, v):
        if v is not None:
            if not v or v.strip() == "":
                raise ValueError("Hostname cannot be empty")
            return v.strip().lower()
        return v

    @field_validator("serial_number")
    @classmethod
    def validate_serial_number(cls, v):
        if v is not None:
            if not v or v.strip() == "":
                raise ValueError("Serial number cannot be empty")
            return v.strip().upper()
        return v


class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DeviceList(BaseModel):
    devices: List[DeviceResponse]
    total: int
    page: int
    size: int
    pages: int


class DeviceVersionInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: uuid.UUID
    device_name: str
    current_version: str
    brand: str
    model: str
    hostname: str
    location: str
    is_active: bool
    last_updated: datetime
