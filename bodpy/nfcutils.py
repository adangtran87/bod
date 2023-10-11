import binascii
import flet as ft
import nfc
import time


class ButtonScanNFC(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tag_id = ""
        self.data_ready = False

    def build(self):
        return ft.ElevatedButton(text="Scan", on_click=self.scan)

    def scan(self, e):
        e.page.show_dialog(ft.AlertDialog(title=ft.Text("Scanning...")))
        self.connect()
        e.page.close_dialog()
        time.sleep(0.5)

        if self.data_ready:
            dlg = ft.AlertDialog(title=ft.Text(f"Card Detected: {self.tag_id}"))
        else:
            dlg = ft.AlertDialog(title=ft.Text("No card detected"))

        e.page.show_dialog(dlg)

    def on_startup(self, targets):
        return targets

    def on_connect(self, tag: nfc.tag.Tag):
        self.tag_id = binascii.hexlify(tag.identifier).decode()
        self.data_ready = True
        return True

    def connect(self, iterations: int = 5, interval: float = 0.5):
        rdwr_options = {
            "targets": ["106A"],
            "on-startup": self.on_startup,
            "on-connect": self.on_connect,
            "iterations": iterations,
            "interval": interval,
        }

        after5s = lambda: time.time() - started > 5
        started: float = time.time()

        with nfc.ContactlessFrontend("tty:USB0:pn532") as clf:
            clf.connect(rdwr=rdwr_options, terminate=after5s)
