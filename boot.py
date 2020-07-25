# microIDE Filename: /boot.py
### This file is executed on every boot (including wake-boot from deepsleep)
import _thread

### NOOB WARNING: DO NOT ADD ANYTHING ELSE HERE !!!
### If boot.py has an error it will break and you are locked out
### Use main.py to run your code.


### Connect to existing Network - input SSID & PASSWORD
def wifi():
  import network
  from time import sleep
  sta_if = network.WLAN(network.STA_IF)
  while True:
    sta_if.active(True)
    sta_if.connect("maxmax3", "s0l0mi02s0l0mi0")
    sleep(5)
    if sta_if.isconnected():
      sleep(300)
### Uncomment to enable
_thread.start_new_thread(wifi,())

### Enable the AP with SSID "microIDE" (IP: 192.168.4.1)
#import network
#ap = network.WLAN(network.AP_IF)
#ap.active(True)
#ap.config(essid="microIDE")


### Creates a Reset - it will reset the chip every 10 minutes
def rst():
  from time import sleep
  sleep(590)
  print("Reset imminent")
  sleep(10)
  import machine
  machine.reset()
#_thread.start_new_thread(rst,())

### Creates a WatchDog and a feeding loop - if _thread hangs it will reset.
def wdt():
  from machine import WDT
  from time import sleep
  wdt=WDT(timeout=10000) #10 seconds of hanging
  while True:
    wdt.feed()
    sleep(1)
_thread.start_new_thread(wdt,())


### This enables the webserver and adds some functions for main.py
from microIDE import wget , epoch ,millis
# wget(filename)    # get a files from https://git.microIDE.com
# epoch()           # UNIX epoch (seconds) - Use for long-term data
# millis()          # Miliseconds since Boot - Use for short-term data
