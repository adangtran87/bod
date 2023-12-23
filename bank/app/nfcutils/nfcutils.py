import binascii
import nfc
from functools import partial
import time
import asyncio


class NfcDevice(object):
    def __init__(self, device_loc: str):
        self.data_valid = False
        self.tag_data = {
            "identifier": "",
        }
        self.device_loc = device_loc

    def _on_startup(self, targets):
        return targets

    def _on_connect(self, tag: nfc.tag.Tag):
        self.tag_data["identifier"] = binascii.hexlify(tag.identifier).decode()
        self.data_valid = True
        return True

    async def has_data(self):
        return self.data_valid

    async def get_data(self):
        self.data_valid = False
        return self.tag_data

    async def connect(
        self, iterations: int = 5, interval: float = 0.5, timeout: int = 5
    ):
        rdwr_options = {
            "targets": ["106A"],
            "on-startup": self._on_startup,
            "on-connect": self._on_connect,
            "iterations": iterations,
            "interval": interval,
        }

        after5s = lambda: time.time() - started > timeout
        started: float = time.time()

        loop = asyncio.get_event_loop()

        # TODO: Do not hardcode device path
        with nfc.ContactlessFrontend(self.device_loc) as clf:
            await loop.run_in_executor(
                None, partial(clf.connect, rdwr=rdwr_options, terminate=after5s)
            )
