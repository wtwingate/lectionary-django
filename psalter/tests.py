from django.test import TestCase
from psalter.services import parse_psalm_num, parse_verse_nums


class PsalterServicesTestCase(TestCase):
    def test_parse_psalm_num(self):
        """Psalm numbers are correctly parsed from references."""

        self.assertEqual(parse_psalm_num("Psalm 23"), 23)
        self.assertEqual(parse_psalm_num("Psalm 23:1-6"), 23)
        self.assertEqual(parse_psalm_num("Psalm 23:1, 2-3, 4-6"), 23)

    def test_parse_verse_nums(self):
        """Sequence of verse numbers are correctly parsed from reference."""

        self.assertEqual(parse_verse_nums("Psalm 23:1"), [1])
        self.assertEqual(parse_verse_nums("Psalm 23:1, 6"), [1, 6])
        self.assertEqual(parse_verse_nums("Psalm 23:1-6"), [1, 2, 3, 4, 5, 6])
        self.assertEqual(parse_verse_nums("Psalm 23:1, (2-3), 4-6"), [1, 2, 3, 4, 5, 6])
