#!/usr/bin/env python3

from random import random
from time import sleep

from gpiozero import DigitalOutputDevice
import smbus

# TODO: remove crystal by generating 1MHz clock on GPIO4 (GPCLK0)

DEVICE: int = 0x27
cs = DigitalOutputDevice(4, active_high=False) #GPIO4

address_map = {
    0x00: 'IODIRA', 0x01: 'IODIRB', 0x02: 'IPOLA', 0x03: 'IPOLB',
    0x04: 'GPINTENA', 0x05: 'GPINTENB', 0x06: 'DEFVALA', 0x07: 'DEVFALB',
    0x08: 'INTCONA', 0x09: 'INTCONB', 0x0a: 'IOCON', 0x0b: 'IOCON',
    0x0c: 'GPPUA', 0x0d: 'GPPUB', 0x0e: 'INTFA', 0x0f: 'INTFB',
    0x10: 'INTCAPA', 0x11: 'INTCAPB', 0x12: 'GPIOA', 0x13: 'GPIOB',
    0x14: 'OLATA', 0x15: 'OLATB'
}
register_map = {value: key for key, value in address_map.items()}
max_len = max(len(key) for key in register_map)


def print_values(bus):
    print("-" * 20)
    for addr in address_map:
        value = bus.read_byte_data(DEVICE, addr)
        print("%-*s = 0x%02X" % (max_len, address_map[addr], value))


bus = smbus.SMBus(1)
def setup():
    bus.write_byte_data(DEVICE, register_map['GPPUA'], 0x00)
    bus.write_byte_data(DEVICE, register_map['GPPUB'], 0x00)
    bus.write_byte_data(DEVICE, register_map['IODIRA'], 0x00) # set GPIOA to output mode
    bus.write_byte_data(DEVICE, register_map['IODIRB'], 0x00) # set GPIOB to output mode

def ping_chip_select():
    cs.on()
    # no need for a delay here
    sleep(.00001)
    cs.off()


def sid_write(addr: int, data: int, ping_cs=True):
    addr = addr % (1<<5)
    data = data % (1<<8)
#    print(f'WRITE data 0X{data:02X} 0b{data:08b} at addr 0X{addr:02X} 0b{addr:05b}')
    bus.write_byte_data(DEVICE, register_map['GPIOB'], addr)
    bus.write_byte_data(DEVICE, register_map['GPIOA'], data)
    if ping_cs:
        ping_chip_select()


def poke(addr, data):
    sid_write(addr, data, ping_cs=True)
    sleep(.001)


def shutdown():
    for addr in range(26):
        sid_write(addr, 0)
    ping_chip_select()
    cs.off()


def rnd_poke():
    """10 POKE 54272 + RND(1) *25, RND(1) * 256 : GOTO 10"""
    sid_write(int(random() * 25), int(random() * 256))
