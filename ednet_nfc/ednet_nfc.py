import reflex as rx

from ednet_nfc.components import (
    conversion_ctas,
    holo_hero,
    media_block,
    social_grid,
    solutions_carousel,
    trajectory,
)
from ednet_nfc.state import LandingState

app = rx.App(
    stylesheets=["/styles.css"],
    theme=rx.theme(appearance="dark", accent_color="teal", radius="large"),
    style={
        "background": "#020617",
        "color": "#e2e8f0",
        "font_family": "Inter, ui-sans-serif, system-ui, sans-serif",
    },
)


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            holo_hero(),
            conversion_ctas(),
            media_block(),
            solutions_carousel(),
            social_grid(),
            trajectory(),
            rx.text(
                "edwuarcardenas.online · ED NET PRO · Cúcuta",
                size="1",
                color="#64748b",
                text_align="center",
            ),
            spacing="4",
            width="100%",
            max_width="440px",
            padding_y="1.5rem",
            padding_x="1rem",
        ),
        min_height="100vh",
        background="#020617",
    )


app.add_page(
    index,
    route="/",
    title="Edwuar Cárdenas | ED NET PRO",
    description="Diseño ecosistemas digitales autónomos e Inteligencia Artificial que convierten visitantes en clientes en tiempo real.",
    on_load=LandingState.on_load,
)
