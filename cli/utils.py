from result import Err, Ok, Result

import bank.app.nfcutils.nfcutils as nfc


async def scan_card(device: str) -> Result[str, str]:
    dev = nfc.NfcDevice(device)
    print("Tap Card:")
    await dev.connect()
    if dev.has_data():
        data = await dev.get_data()
        if data["identifier"] == "":
            return Err("No card detected")
        else:
            return Ok(data["identifier"])
    else:
        return Err("No card detected")
