import bank.app.nfcutils.nfcutils as nfc


async def scan_card(device: str) -> str:
    dev = nfc.NfcDevice(device)
    print("Tap Card:")
    await dev.connect()
    if dev.has_data():
        data = await dev.get_data()
        print(data)
        return ""
    else:
        return ""
