from django.db import models
from django.urls import reverse


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

    name = models.CharField(max_length=256)
    alt_name = models.CharField(max_length=256, null=True, blank=True)
    service = models.CharField(max_length=256, null=True, blank=True)
    year = models.CharField(max_length=1, choices=Year)
    season = models.CharField(max_length=2, choices=Season, null=True, blank=True)

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

    def __str__(self):
        return f"{self.scripture}"
