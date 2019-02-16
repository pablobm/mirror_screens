#!/usr/bin/env python
"""
A Python script to get secondary screens mirroring the primary.

This script uses the `xrandr` tool to figure out what secondary
screens are available, and then maps them (using scaling) over the
portion of X11's virtual screen covered by the primary.
"""
import re
import subprocess

class DisplayInfo:
    def __init__(self, displays):
        self.displays = displays

    @property
    def primary(self):
        return self._find_screen_with_primary_marker() or self._find_first_screen_with_current_mode_marker()

    def _find_screen_with_primary_marker(self):
        try:
            return next(d for d in self.displays if d.marked_primary)
        except StopIteration:
            # No screeen marked as primary
            None

    def _find_first_screen_with_current_mode_marker(self):
        try:
            return next(d for d in self.displays if d.current_mode)
        except StopIteration:
            # No screeen with a mode marked as current
            None

    @property
    def secondaries(self):
        primary = self.primary
        return [d for d in self.displays if d != primary]


class Display:
    def __init__(self):
        self.name = None
        self.marked_primary = False
        self.modes = []

    @property
    def current_mode(self):
        try:
            return next(d for d in self.modes if d.marked_current)
        except StopIteration:
            # No screeen with a mode marked as current
            None

    @property
    def max_mode(self):
        best = None
        max_prod = 0
        for m in self.modes:
            if max_prod < m.w * m.h:
                best = m
                max_prod = m.w * m.h
        return best


class Mode:
    def __init__(self, w, h, marked_current=False):
        self.w = w
        self.h = h
        self.marked_current = marked_current

    def correction_for(self, other):
        return CorrectionFactor(float(self.w) / other.w, float(self.h) / other.h)

    def __str__(self):
        return '%sx%s' % (self.w, self.h)

    def __repr__(self):
        attrs = [repr(self.w), repr(self.h)]
        if self.marked_current:
            attrs.append("marked_current=True")

        _attrs = ", ".join(attrs)
        return "%s(%s)" % (self.__class__.__name__, _attrs)


class CorrectionFactor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '%sx%s' % (self.x, self.y)

def run(line):
    print(line)
    proc = subprocess.Popen(line.split(" "), stdout=subprocess.PIPE)
    return proc.communicate()[0]

def raw_read_current_displays():
    return run('xrandr').decode('utf8')

def parse(input_str):
    displays = []
    for line in input_str.splitlines():
        m = re.search(r'^(\S+) connected (primary)?', line)
        if m:
            display = Display()
            display.name = m.group(1)
            display.marked_primary = bool(m.group(2))
            displays.append(display)
        else:
            m = re.search(r'^\s+(\d+)x(\d+)([* ])[+ ]', line)
            if m:
                width = int(m.group(1))
                height = int(m.group(2))
                marked_current = bool(m.group(3))
                mode = Mode(width, height, marked_current=marked_current)
                display.modes.append(mode)

    return DisplayInfo(displays)

raw_data = raw_read_current_displays()
dinfo = parse(raw_data)
primary = dinfo.primary
pmode = primary.max_mode

run('xrandr --output %s --mode %s --pos 0x0' % (primary.name, pmode))
for d in dinfo.secondaries:
    smode = d.max_mode
    correction = pmode.correction_for(smode)
    run('xrandr --output %s --pos 0x0 --mode %s --scale %s' % (d.name, smode, correction))
