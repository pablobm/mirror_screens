import unittest

import support
import parser

class ParseTest(unittest.TestCase):
    def test_with_labelled_primary(self):
        xrandr_output = support.fixture("small-dell.double.xrandr")
        dinfo = parser.parse(xrandr_output)
        primary = dinfo.primary
        self.assertTrue(primary)
        self.assertEqual(primary.preferred_mode.w, 1280)
        self.assertEqual(primary.preferred_mode.h, 800)

        others = dinfo.secondaries
        self.assertEqual(len(others), 1)

    def test_without_labelled_primary(self):
        xrandr_output = support.fixture("dell-latitude.double.xrandr")
        dinfo = parser.parse(xrandr_output)
        primary = dinfo.primary
        self.assertTrue(primary)
        self.assertEqual(primary.preferred_mode.w, 1440)
        self.assertEqual(primary.preferred_mode.h, 900)

        others = dinfo.secondaries
        self.assertEqual(len(others), 1)

class ParseDisplayLineTest(unittest.TestCase):
    def test_with_primary_marker(self):
        line = "LVDS1 connected primary 1280x800+0+0 (normal left inverted right x axis y axis) 260mm x 160mm"
        display = parser.parse_display_line(line)
        self.assertTrue(display)
        self.assertEqual(display.name, "LVDS1")
        self.assertTrue(display.marked_primary)

    def test_without_primary_marker(self):
        line = "eDP-1 connected 1440x900+0+0 (normal left inverted right x axis y axis) 303mm x 190mm"
        display = parser.parse_display_line(line)
        self.assertTrue(display)
        self.assertEqual(display.name, "eDP-1")
        self.assertFalse(display.marked_primary)

    def test_disconnected_display(self):
        line = "VGA-1 disconnected (normal left inverted right x axis y axis)"
	display = parser.parse_display_line(line)
	self.assertIsNone(display)

    def test_other_line(self):
	line = "Screen 0: minimum 320 x 200, current 1440 x 900, maximum 8192 x 8192"
	display = parser.parse_display_line(line)
	self.assertIsNone(display)


class ParseModeLineTest(unittest.TestCase):
    def test_with_marked_current(self):
	line = "   1440x900      60.00*+  40.00"
        mode = parser.parse_mode_line(line)
        self.assertEqual(mode.w, 1440)
        self.assertEqual(mode.h, 900)
        self.assertTrue(mode.marked_current)

    def test_with_marked_preferred_not_current(self):
	line = "   1920x1080     60.00 +"
        mode = parser.parse_mode_line(line)
        self.assertEqual(mode.w, 1920)
        self.assertEqual(mode.h, 1080)
        self.assertFalse(mode.marked_current)

    def test_with_unmarked(self):
	line = "   800x600       59.86  "
        mode = parser.parse_mode_line(line)
        self.assertEqual(mode.w, 800)
        self.assertEqual(mode.h, 600)
        self.assertFalse(mode.marked_current)
