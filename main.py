# microIDE Filename: /main.py
### This file is executed after boot.py and runs after microIDE
###
### Uncomment the followong resource files  - they are static and won't overwrite
### By default .gz files won't show in the directory
### if these comments turn green the files were implemented correctly

### Modes: Change the color of the editor based on extention
wget('mode-python.js.gz')
#wget('mode-css.js.gz')
#wget('mode-html.js.gz')
#wget('mode-javascript.js.gz')


### Workers: Auto-close brackets, error-check, etc.
#wget('worker-css.js.gz')
#wget('worker-html.js.gz')
#wget('worker-javascript.js.gz')

### More at https://git.microIDE.com
import time
from machine import Pin, I2C
#import network
import socket

led = Pin(2, Pin.OUT)
def pisca(tiempo):
  led.on()
  time.sleep(tiempo)
  led.off()
  time.sleep(tiempo)
  led.on()
  time.sleep(tiempo)
  led.off()
  time.sleep(tiempo)


addr = socket.getaddrinfo('0.0.0.0', 81)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

i2c = I2C(0)
i2c = I2C(1, scl=Pin(5), sda=Pin(4), freq=400000)
print("hola")
print(i2c.scan())

while True:
  cl, addr = s.accept()
  if cl:
    i2c.writeto(40, b'123')
    reading=i2c.readfrom(40, 4)
    humedad = ((reading[0] & 0x3F) * 0x100 + reading[1]) * (100.0 / 16383.0)
    temperatura = 165.0 / 16383.0 * ((reading[2] * 0x100 + (reading[3] & 0xFC)) >> 2) - 40
    print('client connected from', addr)
    print(str(cl.recv(100), 'utf8'))
    print('{:5.3f}'.format(temperatura), '{:5.3f}'.format(humedad))
    cl.send('{:5.3f}'.format(temperatura) +';'+ '{:5.3f}'.format(humedad))
    cl.close()
    pisca(.25)
  time.sleep(.1)
