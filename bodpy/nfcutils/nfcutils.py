import binascii
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

        # TODO: Do not hardcode device path
        with nfc.ContactlessFrontend("tty:USB0:pn532") as clf:
            clf.connect(rdwr=rdwr_options, terminate=after5s)
