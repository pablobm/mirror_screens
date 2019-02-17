import unittest

import support
import parser

class ParseTest(unittest.TestCase):
    def test_with_labelled_primary(self):
        xrandr_output = support.fixture("small-dell.double.xrandr")
        dinfo = parser.parse(xrandr_output)
        primary = dinfo.primary
        self.assertTrue(primary)
        self.assertEqual(primary.max_mode.w, 1280)
        self.assertEqual(primary.max_mode.h, 800)

        others = dinfo.secondaries
        self.assertEqual(len(others), 1)

    def test_without_labelled_primary(self):
        xrandr_output = support.fixture("dell-latitude.double.xrandr")
        dinfo = parser.parse(xrandr_output)
        primary = dinfo.primary
        self.assertTrue(primary)
        self.assertEqual(primary.max_mode.w, 1440)
        self.assertEqual(primary.max_mode.h, 900)

        others = dinfo.secondaries
        self.assertEqual(len(others), 1)

if __name__ == "__main__":
    unittest.main()
