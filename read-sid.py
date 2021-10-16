#!/usr/bin/env python3

import sid-modules

#Call setup function from sid-modules to init the sid
setup()

try:
    #max volume
    poke(24,15)

    #set voice 1 to triangle
    poke(4,16)

    poke(00,0x1C)
    poke(01,0xD6)
except KeyboardInterrupt:
    pass
finally:
    print("Shutting down SID")
    shutdown()
    sleep(.1)
    print('bye')
