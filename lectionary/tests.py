from django.test import TestCase

import datetime as dt

from lectionary.services.lectionary import Lectionary


class MoveableDatesTestCase(TestCase):
    def test_early_easter(self):
        """Correctly identifies moveable dates when Easter is early."""

        lectionary = Lectionary(dt.date(2285, 1, 1))
        expect = {
            "easter_day": dt.date(2285, 3, 22),
            "ash_wednesday": dt.date(2285, 2, 4),
            "pentecost": dt.date(2285, 5, 10),
            "advent_sunday": dt.date(2285, 11, 29),
        }
        self.assertEqual(lectionary.moveable, expect)

    def test_late_easter(self):
        """Correctly identifies moveable dates when Easter is late."""

        lectionary = Lectionary(dt.date(2038, 1, 1))
        expect = {
            "easter_day": dt.date(2038, 4, 25),
            "ash_wednesday": dt.date(2038, 3, 10),
            "pentecost": dt.date(2038, 6, 13),
            "advent_sunday": dt.date(2038, 11, 28),
        }
        self.assertEqual(lectionary.moveable, expect)

    def test_leap_years(self):
        """Calculations properly handle leap years."""

        lectionary = Lectionary(dt.date(2024, 1, 1))
        expect = {
            "easter_day": dt.date(2024, 3, 31),
            "ash_wednesday": dt.date(2024, 2, 14),
            "pentecost": dt.date(2024, 5, 19),
            "advent_sunday": dt.date(2024, 12, 1),
        }
        self.assertEqual(lectionary.moveable, expect)
