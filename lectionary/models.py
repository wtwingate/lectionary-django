from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse

from lectionary.services.scripture import get_esv_html, get_esv_text
from psalter.models import Psalm
from psalter.services import parse_psalm_num


class Day(models.Model):
    """A model representing a specific holy day within the three-year
    liturgical calendar.
    """

    class Year(models.TextChoices):
        A = ("A", "Year A")
        B = ("B", "Year B")
        C = ("C", "Year C")

    class Season(models.TextChoices):
        ADVENT = ("AD", "Advent")
        CHRISTMAS = ("CH", "Christmas")
        EPIPHANY = ("EP", "Epiphany")
        LENT = ("LE", "Lent")
        EASTER = ("EA", "Easter")
        PENTECOST = ("PE", "Pentecost")

    class Color(models.TextChoices):
        VIOLET = ("VI", "Violet")
        WHITE = ("WH", "White")
        GREEN = ("GR", "Green")
        RED = ("RE", "Red")
        ROSE = ("RO", "Rose")
        BLUE = ("BL", "Blue")

    name = models.CharField(max_length=256)
    alt_name = models.CharField(max_length=256, null=True, blank=True)
    service = models.CharField(max_length=256, null=True, blank=True)
    year = models.CharField(max_length=1, choices=Year)
    season = models.CharField(max_length=2, choices=Season, null=True, blank=True)
    color = models.CharField(max_length=2, choices=Color, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        if self.service is not None:
            return f"{self.name}: {self.service} ({self.year})"
        return f"{self.name} ({self.year})"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Lesson(models.Model):
    """A model representing a specific lesson appointed in the
    lectionary for one or more holy days. Note that the scripture field
    may have alternate readings separated by " or ".
    """

    reference = models.CharField(max_length=256)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    esv_html = models.TextField(null=True, blank=True)
    esv_text = models.TextField(null=True, blank=True)
    psalm_html = models.TextField(null=True, blank=True)
    psalm_text = models.TextField(null=True, blank=True)

    def get_html(self):
        if self.reference.startswith("Psalm"):
            self.psalm_cache()
            return self.psalm_html
        else:
            self.esv_cache()
            return self.esv_html

    def get_text(self):
        if self.reference.startswith("Psalm"):
            self.psalm_cache()
            return self.psalm_text
        else:
            self.esv_cache()
            return self.esv_text

    def psalm_cache(self):
        if self.psalm_html and self.psalm_text:
            return

        psalm_num = parse_psalm_num(self.reference)
        psalm = get_object_or_404(Psalm, number=psalm_num)
        self.psalm_html = psalm.get_html(self.reference)
        self.psalm_text = psalm.get_text(self.reference)
        self.save()

    def esv_cache(self):
        if self.esv_html and self.esv_text:
            return

        self.esv_html = get_esv_html(self.reference)
        self.esv_text = get_esv_text(self.reference)
        self.save()

    def clear_cache(self):
        self.esv_html = None
        self.esv_text = None
        self.psalm_html = None
        self.psalm_text = None
        self.save()

    def __str__(self):
        return f"{self.reference}"
