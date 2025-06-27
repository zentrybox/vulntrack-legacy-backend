"""
Scan Endpoints (RESTful, Supabase backend)
- POST   /scans         -> Trigger scan for a device
- POST   /scans/batch   -> Trigger scans for multiple devices
- GET    /scans         -> List/paginate scans (with filters)
- GET    /scans/{id}    -> Get scan details (with results)
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.supabase_client import supabase
from app.core.tasks import scan_web_ai_task

router = APIRouter(prefix="", tags=["scans"])


class ScanRequest(BaseModel):
    device_id: str = Field(
        ...,
        title="Device ID",
        description="UUID del dispositivo a escanear",
        example="99d8b93e-14eb-4000-9681-b0ee16ae6fef",
    )


class ScanBatchRequest(BaseModel):
    device_ids: list[str] = Field(
        ...,
        title="Device IDs",
        description="Lista de UUIDs de dispositivos a escanear",
        example=[
            "99d8b93e-14eb-4000-9681-b0ee16ae6fef",
            "b1b2b3b4-5678-1234-5678-abcdefabcdef",
        ],
    )


# --- POST / ---
@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Disparar escaneo para un dispositivo",
    response_description="Scan iniciado",
)
async def trigger_scan(body: ScanRequest) -> Dict[str, Any]:
    device_id = body.device_id
    devices = supabase.get("devices", params={"id": f"eq.{device_id}"})
    if not devices:
        raise HTTPException(status_code=404, detail="Device not found")
    device = devices[0]
    if not device.get("is_active", True):
        raise HTTPException(status_code=400, detail="Device is inactive")
    scan_id = str(uuid.uuid4())
    scan_payload = {
        "id": scan_id,
        "device_id": device_id,
        "scan_type": "web_ai",
        "status": "in_progress",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "vulnerabilities_found": 0,
    }
    supabase.post("scans", scan_payload)
    # Enqueue Celery task
    scan_web_ai_task.delay(scan_id, device)
    return scan_payload


# --- POST /batch ---
@router.post(
    "/batch",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Disparar escaneos batch",
    response_description="Batch de scans iniciado",
)
async def trigger_batch_scan(body: ScanBatchRequest) -> Dict[str, Any]:
    device_ids = body.device_ids
    if not device_ids or not isinstance(device_ids, list):
        raise HTTPException(
            status_code=400, detail="device_ids must be a list of UUIDs"
        )
    job_id = str(uuid.uuid4())
    initiated_scans = []
    for device_id in device_ids:
        scan_id = str(uuid.uuid4())
        scan_payload = {
            "id": scan_id,
            "device_id": device_id,
            "scan_type": "web_ai",
            "status": "in_progress",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "vulnerabilities_found": 0,
        }
        supabase.post("scans", scan_payload)
        devices = supabase.get("devices", params={"id": f"eq.{device_id}"})
        if devices:
            device = devices[0]
            scan_web_ai_task.delay(scan_id, device)
        initiated_scans.append(scan_payload)
    return {
        "job_id": job_id,
        "message": f"{len(initiated_scans)} scans initiated.",
        "initiated_scans": initiated_scans,
    }


# --- GET / ---
@router.get("/")
def list_scans(
    deviceId: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    scanType: Optional[str] = Query(None),
    page: int = 1,
    limit: int = 10,
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
) -> Dict[str, Any]:
    params = {}
    if deviceId:
        params["device_id"] = f"eq.{deviceId}"
    if status and status != "all":
        params["status"] = f"eq.{status}"
    if scanType and scanType != "all":
        params["scan_type"] = f"eq.{scanType}"
    if startDate:
        params["completed_at"] = f"gte.{startDate}"
    if endDate:
        params["completed_at"] = f"lte.{endDate}"
    offset = (page - 1) * limit
    params["offset"] = offset
    params["limit"] = limit
    scans = supabase.get("scans", params=params)
    total = len(scans)
    return {
        "data": scans,
        "currentPage": page,
        "totalPages": (total // limit) + (1 if total % limit else 0),
        "totalItems": total,
        "itemsPerPage": limit,
    }


# --- GET /{scan_id} ---
@router.get("/{scan_id}")
def get_scan(scan_id: str) -> Dict[str, Any]:
    scans = supabase.get("scans", params={"id": f"eq.{scan_id}"})
    if not scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan = scans[0]
    # Obtener resultados asociados
    results = supabase.get("scan_results", params={"scan_id": f"eq.{scan_id}"})
    scan["results"] = results
    return scan
