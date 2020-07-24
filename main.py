from network import LoRa
import socket
import time
import ubinascii
import struct
from machine import Pin

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)
lora = LoRa(mode=LoRa.LORAWAN)
lora.nvram_restore()

for i in range(8, 72):
    lora.remove_channel(i)

start = 903900000
f_inc = 200000
curr  = start

for i in range(8):
    print(curr)
    lora.add_channel(index=i, frequency=curr, dr_min=0, dr_max=4)
    curr += f_inc

# # create an ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('2601117D'))[0]
nwk_swkey = ubinascii.unhexlify('0547672E917858608AE0E407267E1368')
app_swkey = ubinascii.unhexlify('860EFE85C4860C9C373550CF69C3D7C9')
#
# # join a network using ABP (Activation By Personalization)
if not lora.has_joined():
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))



# create an OTAA authentication parameters
# milton
#app_eui = ubinascii.unhexlify('70B3D57ED001319C')
#app_key = ubinascii.unhexlify('E4563EC2FDEFD153F62ABD097070E2AE')
# otaa
#gax
#app_eui = ubinascii.unhexlify('70B3D57ED0024DB4')
#app_key = ubinascii.unhexlify('A60A4B17D6AD9DFEE262964BD8ADEF52')

# join a network using OTAA (Over the Air Activation)
#if not lora.has_joined():
#    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(0.5)
    print('Not yet joined...')
    pycom.rgbled(0xff0000)
    time.sleep(0.5)
    pycom.rgbled(0x000000)

if lora.has_joined():
    print("CONNECTED!!")
    pycom.rgbled(0x00ff00)
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
# s.setsockopt(socket.SOL_LORA)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
#s.setblocking(True)

# send some data
# while lora.has_joined():


while True:

    s.setblocking(True)
    s.send("asd")
    print("enviando")
    pycom.rgbled(0x00ff00)
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(0.2)
    pycom.rgbled(0x00ff00)
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(0.2)
    pycom.rgbled(0x00ff00)
# make the socket non-blocking
#(because if there's no data received it will block forever...)
    s.setblocking(False)

# get any data received (if any...)
    data = s.recv(64)
    time.sleep(2)
    lora.nvram_save()
    if data:##print(data)
        pycom.rgbled(0x0000ff)
        time.sleep(2)
        print(data)
    time.sleep(57)
