import unittest

from classes import Mode

class ClassesTest(unittest.TestCase):
    def test_msi_u135dx(self):
        primary = Mode(1024, 600)
        secondary = Mode(1920, 1080)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 0.5333, places=3)
        self.assertAlmostEqual(correction.y, 0.5555, places=3)

    def test_dell_latitude_d430(self):
        primary = Mode(1280, 800)
        secondary = Mode(1920, 1080)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 0.6666, places=3)
        self.assertAlmostEqual(correction.y, 0.7407, places=3)

    def test_lenovo_thinkpad_edge(self):
        primary = Mode(1366, 768)
        secondary = Mode(1920, 1080)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 0.7114, places=3)
        self.assertAlmostEqual(correction.y, 0.7111, places=3)

    def test_ibm_thinkpad_t42p(self):
        primary = Mode(1600, 1200)
        secondary = Mode(1920, 1080)
        correction = primary.correction_for(secondary)
        self.assertAlmostEqual(correction.x, 0.833, places=3)
        self.assertAlmostEqual(correction.y, 1.111, places=3)
