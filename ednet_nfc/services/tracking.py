from __future__ import annotations

import hashlib
import os
import time
from typing import Any
from urllib.parse import quote

import httpx

META_PIXEL_ID = os.getenv("META_PIXEL_ID", "TU_PIXEL_ID")
META_TOKEN = os.getenv("META_CAPI_ACCESS_TOKEN", "")
GA4_ID = os.getenv("GA4_MEASUREMENT_ID", "G-XXXXXXXXXX")
GA4_SECRET = os.getenv("GA4_API_SECRET", "")
SITE_URL = os.getenv("SITE_URL", "https://edwuarcardenas.online")

EVENT_MAP = {
    "page_view": ("PageView", "page_view"),
    "download_vcf": ("Contact", "generate_lead"),
    "click_whatsapp": ("Lead", "generate_lead"),
    "click_social": ("ViewContent", "select_content"),
    "view_offer": ("ViewContent", "view_item"),
}


def _sha256(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()


def track_server_event(
    event_name: str,
    *,
    user_agent: str = "",
    client_ip: str = "",
    event_source_url: str = "",
    extra: dict[str, Any] | None = None,
) -> None:
    meta_event, ga_event = EVENT_MAP.get(event_name, ("ViewContent", event_name))
    source_url = event_source_url or SITE_URL
    extra = extra or {}

    if META_TOKEN and META_PIXEL_ID and META_PIXEL_ID != "TU_PIXEL_ID":
        payload = {
            "data": [
                {
                    "event_name": meta_event,
                    "event_time": int(time.time()),
                    "action_source": "website",
                    "event_source_url": source_url,
                    "user_data": {
                        k: v
                        for k, v in {
                            "client_ip_address": client_ip or None,
                            "client_user_agent": user_agent or None,
                        }.items()
                        if v
                    },
                    "custom_data": extra,
                }
            ]
        }
        try:
            with httpx.Client(timeout=6.0) as client:
                client.post(
                    f"https://graph.facebook.com/v21.0/{META_PIXEL_ID}/events",
                    params={"access_token": META_TOKEN},
                    json=payload,
                )
        except Exception:
            pass

    if GA4_SECRET and GA4_ID and GA4_ID != "G-XXXXXXXXXX":
        body = {
            "client_id": hashlib.md5((user_agent or "nfc").encode()).hexdigest(),
            "events": [
                {
                    "name": ga_event,
                    "params": {
                        "engagement_time_msec": 1,
                        "session_id": str(int(time.time())),
                        "label": extra.get("label", event_name),
                        "page_location": source_url,
                    },
                }
            ],
        }
        try:
            with httpx.Client(timeout=6.0) as client:
                client.post(
                    "https://www.google-analytics.com/mp/collect",
                    params={"measurement_id": GA4_ID, "api_secret": GA4_SECRET},
                    json=body,
                )
        except Exception:
            pass

    _ = quote(event_name)
