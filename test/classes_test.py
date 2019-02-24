import unittest

from classes import Mode

class ClassesTest(unittest.TestCase):
    def test_secondary_is_same_ratio_and_larger_than_primary(self):
        primary = Mode(1024, 768)
        secondary = Mode(1280, 960)
        correction = primary.correction_for(secondary)
        self.assertEqual(correction.x, 0.8)
        self.assertEqual(correction.y, 0.8)

    def test_secondary_is_same_ratio_and_smaller_than_primary(self):
        primary = Mode(1024, 768)
        secondary = Mode(768, 576)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 1.333, places=3)
        self.assertAlmostEqual(correction.y, 1.333, places=3)

    def test_secondary_with_wider_ratio_and_generally_larger(self):
        primary = Mode(1024, 768)
        secondary = Mode(1280, 720)
        correction = primary.correction_for(secondary)
        self.assertEqual(correction.x, 0.8)
        self.assertEqual(correction.y, 0.8)

    def test_secondary_with_taller_ratio_and_generally_larger(self):
        primary = Mode(1024, 768)
        secondary = Mode(1280, 1024)
        correction = primary.correction_for(secondary)
        self.assertEqual(correction.x, 0.75)
        self.assertEqual(correction.y, 0.75)

    def test_secondary_with_wider_ratio_and_generally_smaller(self):
        primary = Mode(1280, 1024)
        secondary = Mode(1024, 768)
        correction = primary.correction_for(secondary)
        self.assertEqual(correction.x, 1.25)
        self.assertEqual(correction.y, 1.25)

    def test_secondary_with_taller_ratio_and_generally_smaller(self):
        primary = Mode(1280, 854)
        secondary = Mode(1024, 768)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 1.112, places=3)
        self.assertAlmostEqual(correction.y, 1.112, places=3)

    def test_weird_stuff(self):
        primary = Mode(1280, 1024)
        secondary = Mode(1366, 768)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 0.937, places=3)
        self.assertAlmostEqual(correction.y, 0.937, places=3)

        primary = Mode(1366, 768)
        secondary = Mode(1280, 1024)
        correction = primary.correction_for(secondary)
        self.assertEqual(correction.x, 0.75)
        self.assertEqual(correction.y, 0.75)
