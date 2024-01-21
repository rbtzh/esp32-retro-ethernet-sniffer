#!/usr/bin/env python

INTERFACE_NAME = "wlan0" #use ```ip link``` to find your Interface's name. 
BPF_FILTER = "" #Set this to filter out unwanted packet. leave it blank for all packets.

import time

#  import LED Matrix Driver
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, SPECCY_FONT, TINY_FONT
#import network sniffer
from scapy.all import *

def animation(device, from_y, to_y):
    '''Animate the whole thing, moving it into/out of the abyss.'''
    current_y = from_y
    while current_y != to_y:
        with canvas(device) as draw:
            text(draw, (0+3, current_y), "S", fill="white", font=proportional(TINY_FONT))
            text(draw, (8+3, current_y), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (16+3, current_y), "D", fill="white", font=proportional(TINY_FONT))
            text(draw, (24+3, current_y), "T", fill="white", font=proportional(TINY_FONT))
        time.sleep(0.1)
        current_y += 1 if to_y > from_y else -1
    time.sleep(0.5)

def int_to_binary_array(i):
    binary_array = []
    while i > 0:
        binary_array.insert(0, i % 2)
        i = i // 2
    return binary_array

# text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
# value is a int 
def binaryMatrix(draw, xy, value, fill="white"):
    x, y = xy
    for index in range(len(value)):
        dot_x = x + index % 8
        dot_y = y + index // 8
        if value[index] == 1:
            draw.point((dot_x, dot_y), fill="white")


def main():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=90, blocks_arranged_in_reverse_order=True)
    device.contrast(16)

    animation(device, -3, 1)

    while True:

        pak = sniff(iface=INTERFACE_NAME,filter=BPF_FILTER, count=1)[0]

        srcMAC: str = pak.src
        dstMAC: str = pak.dst
        frameType: int = pak.type

        srcMAC_binaryList = [int(bit) for byte in srcMAC.split(":") for bit in '{:08b}'.format(int(byte, 16))]
        dstMAC_binaryList = [int(bit) for byte in dstMAC.split(":") for bit in '{:08b}'.format(int(byte, 16))]
        frameType_binaryList = int_to_binary_array(frameType)
        
        with canvas(device) as draw:
            binaryMatrix(draw, (0,0), srcMAC_binaryList, fill="white")
            text(draw, (9, -1), "»", fill="white", font=proportional(SPECCY_FONT))
            binaryMatrix(draw, (16,0), dstMAC_binaryList, fill="white")
            binaryMatrix(draw, (24,0), frameType_binaryList, fill="white")

if __name__ == "__main__":
    main()
