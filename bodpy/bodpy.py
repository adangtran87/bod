import flet as ft

from ui.admin_panel import AdminPanel
from ui.shop_panel import ShopPanel
from ui.user_panel import UserPanel


def main(page: ft.Page):
    page.title = "Filial Bank"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Home", content=UserPanel()),
            ft.Tab(text="Shop", content=ShopPanel()),
            ft.Tab(text="Admin", content=AdminPanel()),
        ],
        expand=1,
    )

    page.add(t)


if __name__ == "__main__":
    ft.app(target=main)
