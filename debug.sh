#!/bin/bash

ROM=rom.gba
GDB=arm-none-eabi-gdb
VBA=VisualBoyAdvance

$GDB -ex "target remote | $VBA -4 -Gpipe $ROM" -ex "continue"
