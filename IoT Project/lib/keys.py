import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

WIFI_SSID               = ''
WIFI_PASS               = ''

AIO_SERVER              = "io.adafruit.com"
AIO_PORT                = 1883
AIO_USER                = ""
AIO_KEY                 = ""
AIO_CLIENT_ID           = ubinascii.hexlify(machine.unique_id())
AIO_LIGHTS_FEED         = 'neuhaus/feeds/lights'
AIO_RANDOMS_FEED        = 'neuhaus/feeds/random'
AIO_LIVINGTEMP_FEED     = 'neuhaus/feeds/livingroomtemp'
AIO_LIVINGHUM_FEED      = 'neuhaus/feeds/livingroomhum'
AIO_BATHTEMP_FEED       = 'neuhaus/feeds/bathroomtemp'
AIO_BATHHUM_FEED        = 'neuhaus/feeds/bathroomhum'