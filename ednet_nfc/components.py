import reflex as rx

from ednet_nfc.state import LandingState

GLASS = {
    "class_name": "glass",
    "border_radius": "1.5rem",
    "padding": "1.25rem",
    "width": "100%",
}


def social_toast() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                border_radius="999px",
                background="#10B981",
                class_name="verify-blink",
            ),
            rx.text(LandingState.notice, size="1", color="#d1fae5", weight="medium"),
            spacing="2",
            align="center",
        ),
        class_name="glass social-toast",
        padding="0.7rem 0.95rem",
        border_radius="999px",
        width="100%",
    )


def holo_hero() -> rx.Component:
    return rx.vstack(
        social_toast(),
        rx.cond(
            LandingState.spline_url != "",
            rx.el.iframe(
                src=LandingState.spline_url,
                width="100%",
                height="220px",
                style={"border": "0", "border_radius": "1.25rem"},
            ),
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.cond(
                            LandingState.avatar_url != "",
                            rx.image(
                                src=LandingState.avatar_url,
                                alt="Edwuar Cárdenas",
                                width="112px",
                                height="112px",
                                border_radius="999px",
                                object_fit="cover",
                            ),
                            rx.heading("EC", size="8", color="#6ee7b7"),
                        ),
                        class_name="neon-ring",
                        width="118px",
                        height="118px",
                        border_radius="999px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="linear-gradient(135deg,#10B981,#22D3EE)",
                        padding="3px",
                    ),
                    rx.hstack(
                        rx.heading("Edwuar Cárdenas", size="6", color="white"),
                        rx.icon("badge-check", color="#10B981", class_name="verify-blink"),
                        align="center",
                    ),
                    rx.text(
                        "Arquitecto de Soluciones Tecnológicas & Inteligencia Comercial",
                        size="2",
                        color="#cbd5e1",
                        text_align="center",
                    ),
                    rx.badge("ED NET PRO • Cúcuta, Colombia", color_scheme="green", variant="surface"),
                    rx.text(
                        "Diseño ecosistemas digitales autónomos e Inteligencia Artificial que convierten visitantes en clientes en tiempo real.",
                        size="2",
                        color="#94a3b8",
                        text_align="center",
                    ),
                    spacing="3",
                    align="center",
                ),
                class_name="holo-card glass",
                padding="1.6rem",
                border_radius="1.6rem",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )


def conversion_ctas() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.hstack(
                rx.icon("contact"),
                rx.vstack(
                    rx.text("Guardar Contacto (.vcf dinámico)", weight="bold"),
                    rx.text("Anclaje en la agenda · iPhone y Android", size="1", color="#ecfdf5"),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            on_click=LandingState.download_vcf,
            size="3",
            width="100%",
            background="linear-gradient(90deg,#059669,#06b6d4)",
            color="white",
            border_radius="1rem",
            padding="1.1rem",
        ),
        rx.button(
            rx.hstack(
                rx.icon("message-circle"),
                rx.text("WhatsApp Directo · +57 317 1282856", weight="bold"),
                spacing="3",
            ),
            on_click=LandingState.open_whatsapp("hero"),
            size="3",
            width="100%",
            variant="outline",
            color="#6ee7b7",
            border_color="rgba(16,185,129,0.4)",
            class_name="glass",
            border_radius="1rem",
            padding="1.1rem",
        ),
        spacing="3",
        width="100%",
    )


def social_grid() -> rx.Component:
    items = [
        ("TikTok", "https://www.tiktok.com/@ednetnfc", "@ednetnfc", "play"),
        ("Instagram", "https://www.instagram.com/ednet.nfc", "@ednet.nfc", "camera"),
        ("Facebook", "https://www.facebook.com/share/1EuzFTC6xY/", "ED NET PRO", "share-2"),
        ("YouTube", "https://www.youtube.com/@EDNETNFC", "@EDNETNFC", "video"),
    ]
    return rx.grid(
        *[
            rx.box(
                rx.vstack(
                    rx.icon(icon, color="#6ee7b7"),
                    rx.text(name, weight="bold", color="white"),
                    rx.text(handle, size="1", color="#94a3b8"),
                    spacing="1",
                    align="start",
                ),
                on_click=LandingState.open_social(url, name.lower()),
                class_name="glass",
                padding="1rem",
                border_radius="1.1rem",
                cursor="pointer",
            )
            for name, url, handle, icon in items
        ],
        columns="2",
        spacing="3",
        width="100%",
    )


def solutions_carousel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("SOLUCIONES", size="1", weight="bold", color="#94a3b8", letter_spacing="0.12em"),
                rx.text("Neuro-carrusel", size="1", color="#22d3ee"),
                justify="between",
                width="100%",
            ),
            rx.cond(
                LandingState.current_offer["banner"] != "",
                rx.image(
                    src=LandingState.current_offer["banner"],
                    width="100%",
                    height="120px",
                    object_fit="cover",
                    border_radius="0.9rem",
                ),
            ),
            rx.hstack(
                rx.badge(LandingState.current_offer["badge"], color_scheme="teal"),
                justify="end",
                width="100%",
            ),
            rx.heading(LandingState.current_offer["title"], size="5", color="white"),
            rx.text(LandingState.current_offer["description"], size="2", color="#94a3b8"),
            rx.hstack(
                rx.button("←", on_click=LandingState.prev_slide, variant="soft", color_scheme="gray"),
                rx.button(
                    "Quiero esta solución",
                    on_click=LandingState.consult_current,
                    flex="1",
                    background="#064e3b",
                    color="#6ee7b7",
                ),
                rx.button("→", on_click=LandingState.next_slide, variant="soft", color_scheme="gray"),
                width="100%",
                spacing="2",
            ),
            spacing="3",
            width="100%",
        ),
        **GLASS,
    )


def media_block() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("PRUEBA SOCIAL EN MOVIMIENTO", size="1", weight="bold", color="#94a3b8", letter_spacing="0.1em"),
            rx.cond(
                LandingState.promo != "",
                rx.callout(LandingState.promo, icon="megaphone", color="green"),
            ),
            rx.cond(
                LandingState.youtube_id != "",
                rx.el.iframe(
                    src=LandingState.youtube_embed,
                    width="100%",
                    height="200px",
                    style={"border": 0, "border_radius": "1rem"},
                    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture",
                ),
                rx.cond(
                    LandingState.video_url != "",
                    rx.el.video(
                        src=LandingState.video_url,
                        controls=True,
                        style={"width": "100%", "border_radius": "1rem"},
                    ),
                    rx.text("Video dinámico desde PocketBase cuando exista un registro en nfc_settings.", size="1", color="#64748b"),
                ),
            ),
            spacing="3",
            width="100%",
        ),
        **GLASS,
    )


def trajectory() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.icon("trending-up", color="#10B981"),
                rx.vstack(
                    rx.text("8+ años en ventas consultivas", weight="bold", color="white"),
                    rx.text("Asesor comercial de alto rendimiento.", size="1", color="#94a3b8"),
                    spacing="0",
                ),
                spacing="3",
            ),
            **GLASS,
        ),
        rx.box(
            rx.hstack(
                rx.icon("cpu", color="#22d3ee"),
                rx.vstack(
                    rx.text("Liderazgo en ED NET PRO", weight="bold", color="white"),
                    rx.text("Infraestructura IA, CRM, agentes y marketing de conversión.", size="1", color="#94a3b8"),
                    spacing="0",
                ),
                spacing="3",
            ),
            **GLASS,
        ),
        spacing="3",
        width="100%",
    )
