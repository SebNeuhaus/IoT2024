# boot.py -- run on boot-up

import wifiConnection
import ubinascii              # Conversions between binary data and various encodings

try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")