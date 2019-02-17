import re

from classes import Display, DisplayInfo, Mode

def parse(input_str):
    displays = []
    display = None
    for line in input_str.splitlines():
        maybe_display = parse_display_line(line)
        if maybe_display:
            display = maybe_display
            displays.append(display)
            continue
        mode = parse_mode_line(line)
        if mode:
            display.modes.append(mode)

    return DisplayInfo(displays)

def parse_display_line(line):
    m = re.search(r'^(\S+) connected (primary)?', line)
    if m:
        display = Display()
        display.name = m.group(1)
        display.marked_primary = bool(m.group(2))
        return display

def parse_mode_line(line):
    m = re.search(r'^\s+(\d+)x(\d+)([* ])[+ ]', line)
    if m:
        width = int(m.group(1))
        height = int(m.group(2))
        marked_current = bool(m.group(3))
        mode = Mode(width, height, marked_current=marked_current)
        return mode