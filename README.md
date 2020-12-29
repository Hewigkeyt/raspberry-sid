# raspberry-sid
MOS 6581 SID HAT, chiptune player and synth for Raspberry Pi


## Tools

### Printing SID register dumps

Use hexdump, align to 25 bytes (there are 25 writable registers in the SID)

```
hexdump -e '/0 "%6_ad " 25/1 "%02x " "\n" '
```
