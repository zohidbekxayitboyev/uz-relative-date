import unittest
from datetime import datetime
from uz_date_parser import UzbekDateParser


class TestUzbekDateParser(unittest.TestCase):
    def setUp(self):
        # Fixed reference date: Wednesday, Nov 11, 2026
        self.base_date = datetime(2026, 11, 11, 12, 0, 0)
        self.parser = UzbekDateParser(base_date=self.base_date)

    def test_basic_relative_days(self):
        self.assertEqual(self.parser.parse("kecha to'lov qildim").day, 10)
        self.assertEqual(self.parser.parse("bugun uchrashamiz").day, 11)
        self.assertEqual(self.parser.parse("ertaga yuboraman").day, 12)
        self.assertEqual(self.parser.parse("indinga tayyor bo'ladi").day, 13)

    def test_numeric_offsets(self):
        self.assertEqual(self.parser.parse("3 kun oldin kelgan edi").day, 8)
        self.assertEqual(self.parser.parse("5 kundan keyin qaytaraman").day, 16)
        self.assertEqual(self.parser.parse("2 hafta avval").day, 28)

    def test_weekdays(self):
        # Base is Wednesday (index 2), Friday is index 4 (+2 days -> Nov 13)
        self.assertEqual(self.parser.parse("juma kuni ko'rishamiz").day, 13)
        # Past Monday is index 0 (-2 days -> Nov 9)
        self.assertEqual(self.parser.parse("o'tgan dushanba").day, 9)


if __name__ == "__main__":
    unittest.main()
