#!/usr/bin/env python3
from time import sleep

import sid_modules

#Call setup function from sid-modules to init the sid
sid_modules.setup()

try:
    #max volume
    sid_modules.poke(24,15)

    #set voice 1 to triangle
    sid_modules.poke(4,16)

    sid_modules.poke(0,0x1C)
    sid_modules.poke(1,0xD6)
except KeyboardInterrupt:
    pass
finally:
    print("Shutting down SID")
    sid_modules.shutdown()
    sleep(.1)
    print('bye')
