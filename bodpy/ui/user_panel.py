import asyncio
from enum import Enum

import flet as ft

from nfcutils.nfcutils import NfcDevice


class NfcTileType(Enum):
    SHOW_ID = 0


class NfcTile(ft.UserControl):
    def __init__(self, title: str, tile_type: NfcTileType, transition: float = 0.2):
        super().__init__()
        self.nfc = NfcDevice()
        self.title = title
        self.tile_type = tile_type
        self.transition = transition

    async def _on_click_show_id(self, e):
        await e.page.show_dialog_async(
            ft.AlertDialog(
                modal=True, title=ft.Text("Scan Card", text_align=ft.TextAlign.CENTER)
            )
        )
        await asyncio.sleep(1)
        await self.nfc.connect()
        await e.page.close_dialog_async()
        await asyncio.sleep(self.transition)
        if self.nfc.has_data():
            data = await self.nfc.get_data()
            dlg = ft.AlertDialog(title=ft.Text(f"Card Detected: {data['identifier']}"))
        else:
            dlg = ft.AlertDialog(title=ft.Text("No card detected"))

        await e.page.show_dialog_async(dlg)

    def build(self):
        on_click = self._on_click_show_id
        if self.tile_type == NfcTileType.SHOW_ID:
            on_click = self._on_click_show_id
        return ft.Container(
            content=ft.Text(self.title),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.AMBER,
            width=150,
            height=150,
            border_radius=10,
            on_click=on_click,
        )


class UserPanel(ft.UserControl):
    def build(self):
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        NfcTile(title="Info", tile_type=NfcTileType.SHOW_ID),
                        ft.Container(
                            content=ft.Text("Redeem"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.RED,
                            width=150,
                            height=150,
                            border_radius=10,
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.Text("Non clickable"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.AMBER,
                            width=150,
                            height=150,
                            border_radius=10,
                        ),
                        ft.Container(
                            content=ft.Text("Non clickable"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.AMBER,
                            width=150,
                            height=150,
                            border_radius=10,
                        ),
                    ],
                ),
            ],
        )
