from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import httpx

DEFAULT_BASE = os.getenv("POCKETBASE_URL", "https://pocketbase.edwuarcardenas.online")
FALLBACK_BASE = os.getenv("POCKETBASE_FALLBACK", "http://178.105.48.103:8090")


def _bases() -> list[str]:
    return [b.rstrip("/") for b in (DEFAULT_BASE, FALLBACK_BASE) if b]


def _file_url(base: str, collection: str, record_id: str, filename: str) -> str:
    if not filename:
        return ""
    if filename.startswith("http://") or filename.startswith("https://"):
        return filename
    return f"{base}/api/files/{collection}/{record_id}/{filename}"


def fetch_nfc_settings() -> dict[str, Any]:
    for base in _bases():
        try:
            with httpx.Client(timeout=6.0) as client:
                res = client.get(
                    f"{base}/api/collections/nfc_settings/records",
                    params={"sort": "-updated", "perPage": 1},
                )
                if res.status_code >= 400:
                    continue
                payload = res.json()
                rec = (payload.get("items") or [payload])[0]
                if not rec or not rec.get("id"):
                    continue
                rid = rec["id"]
                return {
                    "avatar_url": rec.get("avatar_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("avatar") or rec.get("foto") or ""),
                    "video_url": rec.get("video_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("video") or ""),
                    "youtube_id": rec.get("youtube_id") or "",
                    "notice": rec.get("notice") or rec.get("aviso") or "",
                    "promo": rec.get("promo") or rec.get("oferta") or "",
                    "spline_url": rec.get("spline_url") or os.getenv("SPLINE_SCENE_URL", ""),
                    "banner_1": rec.get("banner_1_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("banner_1") or ""),
                    "banner_2": rec.get("banner_2_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("banner_2") or ""),
                    "banner_3": rec.get("banner_3_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("banner_3") or ""),
                    "banner_4": rec.get("banner_4_url")
                    or _file_url(base, "nfc_settings", rid, rec.get("banner_4") or ""),
                }
        except Exception:
            continue
    return {}


def log_nfc_event(event_name: str, user_agent: str, referrer: str, extra: dict[str, Any] | None = None) -> None:
    body = {
        "event_name": event_name,
        "user_agent": user_agent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "referrer": referrer or "direct",
        "extra": extra or {},
    }
    for base in _bases():
        try:
            with httpx.Client(timeout=6.0) as client:
                res = client.post(
                    f"{base}/api/collections/nfc_analytics/records",
                    json=body,
                )
                if res.status_code < 400:
                    return
        except Exception:
            continue
