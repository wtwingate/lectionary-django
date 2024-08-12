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
        A = "A"
        B = "B"
        C = "C"

    class Season(models.TextChoices):
        ADVENT = "Advent"
        CHRISTMAS = "Christmas"
        EPIPHANY = "Epiphany"
        LENT = "Lent"
        EASTER = "Easter"
        PENTECOST = "Pentecost"

    class Color(models.TextChoices):
        VIOLET = "violet"
        WHITE = "white"
        GREEN = "green"
        RED = "red"
        ROSE = "rose"
        BLUE = "blue"

    name = models.CharField(max_length=256)
    alt_name = models.CharField(max_length=256, null=True, blank=True)
    service = models.CharField(max_length=256, null=True, blank=True)
    year = models.CharField(max_length=16, choices=Year)
    season = models.CharField(max_length=16, choices=Season, null=True, blank=True)
    color = models.CharField(max_length=16, choices=Color, null=True, blank=True)
    lessons = models.ManyToManyField("Lesson", through="DayLesson")

    def __str__(self):
        if self.service is not None:
            return f"{self.name}: {self.service} ({self.year})"
        return f"{self.name} ({self.year})"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Lesson(models.Model):
    """A model representing a specific lesson appointed in the
    lectionary for one or more holy days. Note that the scripture
    field may have alternate readings separated by " or ".
    """

    reference = models.CharField(max_length=256)
    html = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def get_html(self):
        if self.reference.startswith("Psalm"):
            self.psalm_cache()
        else:
            self.esv_cache()
        return self.html

    def get_text(self):
        if self.reference.startswith("Psalm"):
            self.psalm_cache()
        else:
            self.esv_cache()
        return self.text

    def psalm_cache(self):
        if self.html and self.text:
            return

        psalm_num = parse_psalm_num(self.reference)
        psalm = get_object_or_404(Psalm, number=psalm_num)
        self.html = psalm.get_html(self.reference)
        self.text = psalm.get_text(self.reference)
        self.save()

    def esv_cache(self):
        if self.html and self.text:
            return

        self.html = get_esv_html(self.reference)
        self.text = get_esv_text(self.reference)
        self.save()

    def clear_cache(self):
        self.html = None
        self.text = None
        self.save()

    def __str__(self):
        return f"{self.reference}"


class DayLesson(models.Model):
    """A model representing the many-to-many relationship between
    Days and Lessons.
    """

    day = models.ForeignKey("Day", on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)


class Collect(models.Model):
    """A model representing the collect appointed for a given day
    in the lectionary.
    """

    day = models.ForeignKey("Day", on_delete=models.CASCADE)
    text = models.TextField()
