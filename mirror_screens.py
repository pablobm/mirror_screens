#!/usr/bin/env python
"""
A Python script to get secondary screens mirroring the primary.

This script uses the `xrandr` tool to figure out what secondary
screens are available, and then maps them (using scaling) over the
portion of X11's virtual screen covered by the primary.
"""
import subprocess

import parser


def run(line):
    print(line)
    proc = subprocess.Popen(line.split(" "), stdout=subprocess.PIPE)
    return proc.communicate()[0]

def raw_read_current_displays():
    return run('xrandr').decode('utf8')

raw_data = raw_read_current_displays()
dinfo = parser.parse(raw_data)
primary = dinfo.primary
pmode = primary.preferred_mode

run('xrandr --output %s --mode %s --pos 0x0' % (primary.name, pmode))
for d in dinfo.secondaries:
    smode = d.preferred_mode
    correction = pmode.correction_for(smode)
    run('xrandr --output %s --pos 0x0 --mode %s --scale %s' % (d.name, smode, correction))
