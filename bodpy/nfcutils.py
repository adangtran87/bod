import binascii
import flet as ft
import nfc
import time


class NfcDevice(object):
    def __init__(
        self,
    ):
        self.data_valid = False
        self.tag_data = {
            "identifier": "",
        }

    def _on_startup(self, targets):
        return targets

    def _on_connect(self, tag: nfc.tag.Tag):
        self.tag_data["identifier"] = binascii.hexlify(tag.identifier).decode()
        self.data_valid = True
        return True

    def has_data(self):
        return self.data_valid

    def get_data(self):
        self.data_valid = False
        return self.tag_data

    def connect(self, iterations: int = 5, interval: float = 0.5, timeout: int = 5):
        rdwr_options = {
            "targets": ["106A"],
            "on-startup": self._on_startup,
            "on-connect": self._on_connect,
            "iterations": iterations,
            "interval": interval,
        }

        after5s = lambda: time.time() - started > timeout
        started: float = time.time()

        with nfc.ContactlessFrontend("tty:USB0:pn532") as clf:
            clf.connect(rdwr=rdwr_options, terminate=after5s)


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
