#!/usr/bin/env python3
import smbus
import time

DEVICE: int = 0x27

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
bus.write_byte_data(DEVICE, register_map['GPPUA'], 0x00)
bus.write_byte_data(DEVICE, register_map['GPPUB'], 0x00)
bus.write_byte_data(DEVICE, register_map['IODIRA'], 0x00) # set GPIOA to output mode
bus.write_byte_data(DEVICE, register_map['IODIRB'], 0x00) # set GPIOB to output mode


counter = 0
led = False
try:
    while True:
#        print_values(bus)
        counter += 1
        print("counter = %s" % counter)
        if led:
            print("leds on")
            bus.write_byte_data(DEVICE, register_map['GPIOA'], 0xFF)
        else:
            print("leds off")
            bus.write_byte_data(DEVICE, register_map['GPIOA'], 0x00)
        led = not led
        time.sleep(0.25)
except KeyboardInterrupt:
    print("stopping")
