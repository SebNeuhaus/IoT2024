import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import random                 # Random number generator
from machine import Pin, I2C  # Define pin, use I2C
import keys                   # Contain all keys used here
import wifiConnection         # Contains functions to connect/disconnect from WiFi 
import dht
from ssd1306 import SSD1306_I2C


# BEGIN SETTINGS
# These need to be change to suit your environment
TEMP_INTERVAL = 60000       # milliseconds
last_livingroom_temp_sent_ticks = 0 # milliseconds
led = Pin("LED", Pin.OUT)   # led pin initialization for Raspberry Pi Pico W
tempSensor = dht.DHT11(machine.Pin(22))
i2c0 = I2C(0, sda=Pin(16), scl=Pin(17))
display = SSD1306_I2C(128, 64, i2c0)

# Function to display measured temperature & humidity-values on SSD1306 OLED display
def display_temperature(temp, hum):
    try:
        display.fill(0)
        display.text("Temperatur: {} C".format(temp), 1, 20)
        display.text("Fuktighet:  {} %".format(hum), 1, 40)
        display.show()

    except Exception as e:
        print("DISPLAY FAILED")

# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        led.on()                 # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        led.off()                # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.

def send_temperature():
    global last_livingroom_temp_sent_ticks
    global TEMP_INTERVAL

    if ((time.ticks_ms() - last_livingroom_temp_sent_ticks) < TEMP_INTERVAL):
        return; # too soon

    try:
        tempSensor.measure()                # get measurement of temperature and humidity
        temp = tempSensor.temperature()     # store temperature in variable
        hum = tempSensor.humidity()         # store humidity in variable
        display_temperature(temp, hum)      # send measured values to OLED display for "offline" viewing

        # try to publish the temperature to Adafruit IO
        print("Publishing: {0} to {1} ... ".format(temp, keys.AIO_LIVINGTEMP_FEED), end='')
        client.publish(topic=keys.AIO_LIVINGTEMP_FEED, msg=str(temp))

        # try to publish the humidity to Adafruit IO
        print("Publishing: {0} to {1} ... ".format(hum, keys.AIO_LIVINGHUM_FEED), end='')
        client.publish(topic=keys.AIO_LIVINGHUM_FEED, msg=str(hum))


    except Exception as e:
        print("FAILED")
    finally:
        last_livingroom_temp_sent_ticks = time.ticks_ms()
    

# Try WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(keys.AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (keys.AIO_SERVER, keys.AIO_LIGHTS_FEED))



try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever
        client.check_msg()# Action a message if one is received. Non-blocking.
        send_temperature()
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO.")