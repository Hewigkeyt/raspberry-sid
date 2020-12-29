# raspberry-sid
MOS 6581 SID HAT, chiptune player and synth for Raspberry Pi

## Known issues

Some parts of "Cybernoid II" by Jeroen Tel sound strange

## Tools

### Dumping SID registers from `.sid` files

Use [`siddump`, I forked it to add a register dump tool](https://github.com/LIII-XXII/siddump/tree/register-dump)

The current output format is as follows:

- lines of `{mm}:{ss}:{ms/20} {addr} {data}` where 
  - `mm`, `ss`, and `ms/20` are respectively minutes, seconds and 20ths of a millisecond
  - `addr` and `data` are address and data (modulo 256) for the sid registers

### Printing SID register dumps

Use hexdump, align to 25 bytes (there are 25 writable registers in the SID)

```
hexdump -e '/0 "%6_ad " 25/1 "%02x " "\n" '
```
