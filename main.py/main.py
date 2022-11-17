"""
#########################################################
#ky006.py
from machine import Pin, PWM
from utime import sleep

class PassiveBuzzer:
    def buzz():
        ky006 = PWM(Pin(0))
        ky006.freq(500)
        ky006.duty_u16(1000)
        sleep(1)
        ky006.duty_u16(0)
#########################################################
#Temperatura y Humedad
"""
MicroPython Aosong DHT12 I2C driver
"""

class DHTBaseI2C:
    def __init__(self, i2c, addr=0x5c):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
    def measure(self):
        buf = self.buf
        self.i2c.readfrom_mem_into(self.addr, 0, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception("checksum error")

class DHT12(DHTBaseI2C):
    def humidity(self):
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

pin=Pin(16,Pin.IN)

class Temperatura:
    def Temp():
        #utime.sleep(1)
        data_dht=DHT12(pin)
        temp=(data_dht.temperature)
        humidity=(data_dht.humidity)
        print("temperature(C):{}".format(temp))
        print("humidity(%): {}".format(humidity))
##########################################################
#tpw color
from machine import Pin
import time

ledR = Pin(18, Pin.OUT)
ledG = Pin(19, Pin.OUT)

class TwoColor:
    def Two():
        ledR.toggle
        print("Color change")  
        ledG.toggle()  
        time.sleep(3) 
#######################
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
#from secrets import secrets
import socket
#from ky006 import PassiveBuzzer

# Set country to avoid possible errors
rp2.country('DE')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = 'SoyBastidas'
pw = 'B653F943B2F3B27D'

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)
#buzz = PWM(Pin(0))

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        led_Buzz = r.find('?buzz=on')
        led_temp = r.find('?temp=on')
        led_tcolor = r.find('?two=on')
        
        print('led_buzz = ', led_Buzz)
        if led_Buzz > -1:
            print('BUZZ ON')
            #led.value(1)
            PassiveBuzzer.buzz()
            
        print('led_temp = ', led_temp)
        if led_temp > -1:
            print('TEMP ON')
            #led.value(1)
            Temperatura.Temp()
        
        print('led_tcolor = ', led_tcolor)
        if led_tcolor > -1:
            print('TWOCOLOR ON')
            #led.value(1)
            TwoColor.Two()
  
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()
"""
