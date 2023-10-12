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
