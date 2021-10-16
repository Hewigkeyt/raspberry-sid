#!/bin/env sh
# siddump.sh
# helper for siddump.exe: dump all writes to sid chip

FILEIN="$1"
FILEOUT="${2:-"$(basename "$1").dmp.txt"}"
TOOL="$HOME/siddump/siddump.exe"

echo "$(basename "$TOOL") $FILEIN > $FILEOUT"
"$TOOL" "$FILEIN" -s -t300 | grep -e "^[0-9]" > "$FILEOUT"
