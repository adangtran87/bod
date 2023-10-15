# Filial Bank
System for tracking fake currency through RFID cards

```
make run
```

# Setup
## Development
- Connect PN532 UART to FTDI

```
# Create venv
python -m venv ~/.venv/filialbank

# Install dependencies
pip install -r requirements.txt
```

### WSL Host
- Mount FTDI into WSL guest using usbipd

```
usbipd wsl list
usbipd wsl attach --busid <bus_id>

# Example
4-2    0403:6001  USB Serial Converter                                          Attached - WSL
```

### WSL Guest
```
# Verify that you can see FTDI
ls -al /dev/ttyUSB*

# Add your user to dialout group
sudo usermod -a -G dialout $USER

# Set permissions
make wsl
```

# Weirdness
- PC -> FTDI -> PN532 didn't reliably after the first connection. Always got a
  connection error timeout
  - Need to use PC -> USB3 HUB -> FTDI -> PN532

```
(bod) ➜  bod git:(e8bb7ba) make run
python bodpy/bodpy.py

(flet:27165): Gdk-CRITICAL **: 23:41:22.177: gdk_window_get_state: assertion 'GDK_IS_WINDOW (window)' failed
Exception in thread Thread-17:
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/flet_core/event_handler.py", line 28, in __sync_handler
    h(r)
  File "/home/alex/git/bod/bodpy/ui/user_panel.py", line 27, in _on_click_show_id
    self.nfc.connect()
  File "/home/alex/git/bod/bodpy/nfcutils/nfcutils.py", line 43, in connect
    with nfc.ContactlessFrontend("tty:USB0:pn532") as clf:
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/nfc/clf/__init__.py", line 75, in __init__
    if path and not self.open(path):
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/nfc/clf/__init__.py", line 149, in open
    self.device = device.connect(path)
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/nfc/clf/device.py", line 112, in connect
    device = driver.init(tty)
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/nfc/clf/pn532.py", line 411, in init
    if not transport.read(timeout=initial_timeout) == Chipset.ACK:
  File "/home/alex/.venv/bod/lib/python3.8/site-packages/nfc/clf/transport.py", line 154, in read
    raise IOError(errno.ETIMEDOUT, os.strerror(errno.ETIMEDOUT))
```
