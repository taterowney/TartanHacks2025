import board
import neopixel
import smbus
# -*- coding:utf-8 -*-
import time

address = 0x13

bus = smbus.SMBus(1)

p = neopixel.NeoPixel(board.D18, 50)
p.fill((128, 128, 128))
while True:
    if bus.read_byte(address) >= 0x20:
        p.fill((0,0,0))
    time.sleep(0.5)