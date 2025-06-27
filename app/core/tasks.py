import asyncio
import logging
from datetime import datetime, timezone

from app.core.celery_app import celery_app
from app.core.supabase_client import supabase
from app.services.vulnerability_scanner import vulnerability_scanner


@celery_app.task(name="scan.web_ai")
def scan_web_ai_task(scan_id, device):
    return run_web_ai_scan(scan_id, device)


def run_web_ai_scan(scan_id, device):
    """
    Ejecuta el escaneo web_ai y actualiza Supabase (sincrónico para Celery).
    - Registra vulnerabilidad en 'vulnerabilities' si no existe (por cve_id)
    - Inserta resultado en 'scan_results' usando el id (uuid) correcto
    - Notifica al usuario dueño del dispositivo en 'notifications'
    - Actualiza ai_summary y ai_recommendations en scans
    Retorna resumen para logging de Celery.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        scan_result = loop.run_until_complete(vulnerability_scanner.scan_device(device))
        ai_summary = scan_result.get("ai_summary", scan_result.get("summary", ""))
        ai_recommendations = scan_result.get("ai_recommendations", "")
        update_fields = {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "summary": ai_summary,  # ahora el resumen IA va en summary
            "ai_recommendations": ai_recommendations,
        }
        confidence_score = scan_result.get("confidence_score")
        if confidence_score is not None:
            try:
                update_fields["ai_confidence_score"] = float(confidence_score)
            except Exception:
                pass
        vulns = scan_result.get("vulnerabilities", [])
        update_fields["vulnerabilities_found"] = len(vulns)
        logging.warning(f"PATCH scans {scan_id} payload: {update_fields}")
        supabase.patch("scans", {"id": scan_id}, update_fields)
        for vuln in scan_result.get("vulnerabilities", []):
            cve_id = vuln.get("cve_id")
            vuln_id = None
            # Completa campos vacíos con valores por defecto
            description = vuln.get("description", "No description provided.")
            severity = vuln.get("severity") or "Informational"
            if severity.lower() in ["unknown", "uknown", "", None]:
                severity = "Informational"
            remediation = vuln.get("remediation") or "No remediation provided."
            affected_software = vuln.get("affected_software") or "Not specified."
            reference_links = vuln.get("reference_links") or []
            name = vuln.get("name", cve_id or "Unnamed Vulnerability")
            # ...existing code...
            if cve_id:
                existing = supabase.get(
                    "vulnerabilities", params={"cve_id": f"eq.{cve_id}"}
                )
                if not existing:
                    vuln_payload = {
                        "cve_id": cve_id,
                        "name": name,
                        "description": description,
                        "severity": severity,
                        "cvss_score": vuln.get("cvss_score"),
                        "remediation": remediation,
                        "affected_software": affected_software,
                        "reference_links": reference_links,
                    }
                    inserted = supabase.post("vulnerabilities", vuln_payload)
                    if inserted and isinstance(inserted, list) and inserted:
                        vuln_id = inserted[0].get("id")
                else:
                    vuln_id = existing[0].get("id")
            # 2. Registrar resultado del scan
            result_payload = {
                "scan_id": scan_id,
                "vulnerability_id": vuln_id,
                "finding": description,
                "details": str(vuln.get("details", "")),
                "severity": severity,
                "status": "open",
                "ai_confidence_score": float(scan_result.get("confidence_score", 0.0)),
                "ai_suggested_remediation": remediation,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            supabase.post("scan_results", result_payload)
        # 3. Registrar notificación al usuario dueño del dispositivo
        user_id = device.get("user_id")
        if user_id:
            notif_payload = {
                "user_id": user_id,
                "type": "scan_completed",
                "title": f"Escaneo completado para {device.get('name', device.get('hostname', 'dispositivo'))}",
                "message": f"El escaneo ha finalizado. Vulnerabilidades encontradas: {len(scan_result.get('vulnerabilities', []))}",
                "is_read": False,
                "link": f"/scans/{scan_id}",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            supabase.post("notifications", notif_payload)
        return {
            "scan_id": scan_id,
            "vulnerabilities_found": len(scan_result.get("vulnerabilities", [])),
            "status": "completed",
        }
    except Exception as e:
        supabase.patch(
            "scans", {"id": scan_id}, {"status": "failed", "summary": str(e)}
        )
        return {"scan_id": scan_id, "status": "failed", "error": str(e)}
