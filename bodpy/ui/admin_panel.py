import asyncio

import flet as ft

from nfcutils.nfcutils import NfcDevice


class ButtonGetNfcId(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.nfc = NfcDevice()

    def build(self):
        return ft.ElevatedButton(text="Get NFC Id", on_click=self.scan)

    async def scan(self, e):
        await e.page.show_dialog_async(ft.AlertDialog(title=ft.Text("Scanning...")))
        await self.nfc.connect()
        await e.page.close_dialog_async()
        await asyncio.sleep(0.5)

        if self.nfc.has_data():
            data = await self.nfc.get_data()
            dlg = ft.AlertDialog(title=ft.Text(f"Card Detected: {data['identifier']}"))
        else:
            dlg = ft.AlertDialog(title=ft.Text("No card detected"))

        await e.page.show_dialog_async(dlg)


class AdminPanel(ft.UserControl):
    def build(self):
        return [
            ft.Container(
                margin=10,
                padding=10,
                content=ft.Row(
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ButtonGetNfcId(), ButtonGetNfcId()],
                ),
            )
        ]
