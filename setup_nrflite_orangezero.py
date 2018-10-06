#!/usr/bin/env python3
import time
import smbus

bus = smbus.SMBus(1)  # Puerto i2c-1 auxiliar de la Orange Pi Zero H2
address = 0x10        # Dirección por defecto esclavo (no modificable)
channel = 100		  # 0-125 (2400 - 2525 MHz)
bitrate = 2			  # 2 => BITRATE2MBPS, 1 => BITRATE1MBPS, 0 = > BITRATE250KBPS

# Config remote device
try:
    bus.write_i2c_block_data(address, 'b', [bitrate, 'c', channel])
    time.sleep(10)                    #delay ten seconds to reboot remote device
    print("Config OK")
except KeyboardInterrupt:
    print("Config FAIL")
    quit()