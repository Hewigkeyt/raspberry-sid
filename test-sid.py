#!/usr/bin/env python3

from random import seed, random
from time import sleep, time

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

setup()

def ping_chip_select():
    cs.on()
    sleep(.000002)
    cs.off()


def sid_write(addr: int, data: int, ping_cs=True):
    addr = addr % (1<<5)
    data = data % (1<<8)
    #print(f'WRITE data 0X{data:02X} 0b{data:08b} at addr 0X{addr:02X} 0b{addr:05b}')
    bus.write_byte_data(DEVICE, register_map['GPIOB'], addr)
    bus.write_byte_data(DEVICE, register_map['GPIOA'], data)
    if ping_cs:
      ping_chip_select()


def poke(addr, data):
    sid_write(addr, data, ping_cs=True)
    sleep(.001)


def shutdown():
    sid_write(0, 0, False)
    cs.off()


def rnd_poke():
    """10 POKE 54272 + RND(1) *25, RND(1) * 256 : GOTO 10"""
    sid_write(int(random() * 25), int(random() * 256))


def sid_bench():
    """basic SID benchmark
    http://ploguechipsounds.blogspot.com/2010/05/one-page-basic-sid-benchmark.html
120 v(0)=54272:v(1)=54279:v(2)=54286
130 poke54296,15:fori=0to2
140 pokev(i)+3,8:pokev(i)+1,0
150 pokev(i)+5,8:pokev(i)+6,198:next
160 fora=16to128step16:fori=0to2
170 if a>64 then pokev(i)+3,0
180 pokev(i)+4,a+1
190 forf=0to254step2:pokev(i)+1,f:nextf
200 pokev(i)+4,a:forw=0to200:nextw
210 pokev(i)+4,8:pokev(i)+1,0
220 nexti,a:a=1
230 fori=0to2:pokev(i)+1,255
240 poke54296,(a*16)+15:poke54295,2^i
250 pokev(i)+4,129
260 forf=0to255:poke54294,f:nextf
270 pokev(i)+4,136:nexti
280 a=a*2:if a<8 then goto 230
310 poke54295,0
    """
    # 54272 is a multiple of 256 so we can use the register addresses directly
    bench_start = time()

    L=.15

    v = [54272, 54279, 54286] # 120

    print('part1')
    poke(54296, 15)
    for i in range(3): # 130
        poke(v[i] + 3,   8) # 140
        poke(v[i] + 1,   0)
        sleep(L)
        poke(v[i] + 5,   8) # 150
        poke(v[i] + 6, 198)
        sleep(L)
    sleep(L)
    for a in range(16, 129, 16): # 160
        for i in range(3):
            if a > 64:
                poke(v[i] + 3, 0) # 170
            sleep(L)
            poke(v[i] + 4, a + 1) # 180
            sleep(L)
            for f in range(0, 255, 2): # 190
                poke(v[i] + 1, f)
            sleep(L)
            poke(v[i] + 4, a) # 200
            sleep(L)
            poke(v[i] + 4, 8) # 210
            poke(v[i] + 1, 0)
            sleep(L)
    print('part2')
    a=1 # 220
    while True:
        for i in range(3):
            poke(v[i] + 1, 255) # 230
            sleep(L)
            poke(54296, (a*16)+15) # 240
            poke(54295, 2**i)
            sleep(L)
            poke(v[i] + 4, 129) # 250
            sleep(L)
            for f in range(256): # 260
                poke(54294, f)
            sleep(L)
            poke(v[i]+4, 136) # 270
            sleep(L)
        a = a * 2
        if a >= 8:
            break
    poke(54295, 0)

    print(f'bench took {time() - bench_start:.1f}s')
    return


counter = 0
time_start = time()
try:
    print('sid_bench')
    sid_bench()
    print('done')

    sleep(3)

    print('10 poke 54272+int(rnd(1)*25),int(rnd(1)*256) : goto 10')
    seed(1)
    while True:
        counter += 1
        print(f"counter = {counter} {time() - time_start:.3f}")
        rnd_poke()
        sleep(0.05)
except KeyboardInterrupt:
    print("Shutting down SID")
    shutdown()
