import flet as ft

from ui.admin_panel import AdminPanel


def main(page: ft.Page):
    page.title = "Bank of Dad"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.add(AdminPanel())


if __name__ == "__main__":
    ft.app(target=main)
