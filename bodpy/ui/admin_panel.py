import time

import flet as ft

from nfcutils.nfcutils import NfcDevice


class ButtonGetNfcId(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.nfc = NfcDevice()

    def build(self):
        return ft.ElevatedButton(text="Get NFC Id", on_click=self.scan)

    def scan(self, e):
        e.page.show_dialog(ft.AlertDialog(title=ft.Text("Scanning...")))
        self.nfc.connect()
        e.page.close_dialog()
        time.sleep(0.5)

        if self.nfc.has_data():
            data = self.nfc.get_data()
            dlg = ft.AlertDialog(title=ft.Text(f"Card Detected: {data['identifier']}"))
        else:
            dlg = ft.AlertDialog(title=ft.Text("No card detected"))

        e.page.show_dialog(dlg)


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
