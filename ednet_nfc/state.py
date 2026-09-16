from __future__ import annotations

import os
from urllib.parse import quote

import reflex as rx
from dotenv import load_dotenv

from ednet_nfc.services.pocketbase import fetch_nfc_settings, log_nfc_event
from ednet_nfc.services.tracking import track_server_event

load_dotenv()

WA_TEXT = (
    "Hola Edwuar, vengo de tu tarjeta NFC. Quiero diseñar un ecosistema digital "
    "autónomo con IA para convertir visitantes en clientes."
)
WA_URL = f"https://wa.me/573171282856?text={quote(WA_TEXT)}"

DEFAULT_OFFERS = [
    {
        "title": "Tarjetas NFC Inteligentes",
        "description": "Landing ultra premium + vCard dinámico. El primer contacto físico que abre un embudo autónomo.",
        "badge": "$250.000 COP",
        "icon": "nfc",
        "banner": "",
    },
    {
        "title": "CRM Automatizado",
        "description": "PocketBase + n8n + WhatsApp Bot. Captura, califica y hace follow-up sin fricción humana.",
        "badge": "n8n + PocketBase",
        "icon": "workflow",
        "banner": "",
    },
    {
        "title": "Agentes de Voz IA",
        "description": "Atención 24/7 con Vapi / Evolution API. Voz que agenda, responde y cierra.",
        "badge": "Vapi / Evolution",
        "icon": "audio-lines",
        "banner": "",
    },
    {
        "title": "Embudos de Conversión",
        "description": "Meta CAPI + GA4 + tráfico pago. Medición server-side para campañas que venden.",
        "badge": "CAPI + GA4",
        "icon": "target",
        "banner": "",
    },
]


class LandingState(rx.State):
    avatar_url: str = ""
    video_url: str = ""
    youtube_id: str = ""
    notice: str = "3 empresarios de Cúcuta interactuaron hoy con este perfil."
    promo: str = ""
    spline_url: str = os.getenv("SPLINE_SCENE_URL", "")
    slide: int = 0
    offers: list[dict[str, str]] = DEFAULT_OFFERS
    show_toast: bool = True

    def _ua(self) -> str:
        try:
            return self.router.headers.user_agent or ""
        except Exception:
            return ""

    def _ip(self) -> str:
        try:
            return getattr(self.router.session, "client_ip", "") or ""
        except Exception:
            return ""

    def _ref(self) -> str:
        try:
            return self.router.page.raw_path or "direct"
        except Exception:
            return "direct"

    def _track(self, event_name: str, extra: dict | None = None) -> None:
        ua = self._ua()
        log_nfc_event(event_name, ua, self._ref(), extra)
        track_server_event(
            event_name,
            user_agent=ua,
            client_ip=self._ip(),
            extra=extra or {},
        )

    @rx.event
    def on_load(self):
        self._track("page_view")
        data = fetch_nfc_settings()
        if not data:
            return
        self.avatar_url = data.get("avatar_url", "")
        self.video_url = data.get("video_url", "")
        self.youtube_id = data.get("youtube_id", "")
        if data.get("notice"):
            self.notice = data["notice"]
        self.promo = data.get("promo", "")
        if data.get("spline_url"):
            self.spline_url = data["spline_url"]
        banners = [
            data.get("banner_1", ""),
            data.get("banner_2", ""),
            data.get("banner_3", ""),
            data.get("banner_4", ""),
        ]
        updated = []
        for i, offer in enumerate(self.offers):
            item = dict(offer)
            if i < len(banners) and banners[i]:
                item["banner"] = banners[i]
            updated.append(item)
        self.offers = updated

    @rx.var
    def current_offer(self) -> dict[str, str]:
        if not self.offers:
            return {}
        return self.offers[self.slide % len(self.offers)]

    @rx.var
    def youtube_embed(self) -> str:
        if not self.youtube_id:
            return ""
        return f"https://www.youtube.com/embed/{self.youtube_id}?rel=0"

    @rx.event
    def next_slide(self):
        if self.offers:
            self.slide = (self.slide + 1) % len(self.offers)
            self._track("view_offer", {"label": self.current_offer.get("title", "")})

    @rx.event
    def prev_slide(self):
        if self.offers:
            self.slide = (self.slide - 1) % len(self.offers)
            self._track("view_offer", {"label": self.current_offer.get("title", "")})

    @rx.event
    def download_vcf(self):
        self._track("download_vcf", {"label": "Contact"})
        vcard = "\r\n".join(
            [
                "BEGIN:VCARD",
                "VERSION:3.0",
                "N:Cárdenas;Edwuar;;;",
                "FN:Edwuar Cárdenas",
                "ORG:ED NET PRO",
                "TITLE:Arquitecto de Soluciones Tecnológicas & Inteligencia Comercial",
                "TEL;TYPE=CELL,VOICE:+573171282856",
                "URL:https://edwuarcardenas.online",
                "ADR;TYPE=WORK:;;Cúcuta;Norte de Santander;;Colombia",
                "NOTE:Diseño ecosistemas digitales autónomos e Inteligencia Artificial que convierten visitantes en clientes en tiempo real.",
                "END:VCARD",
            ]
        )
        return rx.download(data=vcard, filename="Edwuar_Cardenas_ED_NET_PRO.vcf")

    @rx.event
    def open_whatsapp(self, label: str = "hero"):
        self._track("click_whatsapp", {"label": label})
        return rx.redirect(WA_URL, is_external=True)

    @rx.event
    def consult_current(self):
        label = "solucion"
        if self.offers:
            label = self.offers[self.slide % len(self.offers)].get("title", label)
        self._track("click_whatsapp", {"label": label})
        return rx.redirect(WA_URL, is_external=True)

    @rx.event
    def open_social(self, url: str, network: str):
        self._track("click_social", {"label": network})
        return rx.redirect(url, is_external=True)
