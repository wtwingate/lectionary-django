from django.db import models


class Psalm(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=256)

    def __str__(self):
        return f"Psalm {self.number}"


class Verse(models.Model):
    number = models.IntegerField()
    first_half = models.TextField()
    second_half = models.TextField()
    psalm = models.ForeignKey(Psalm)

    def __str__(self):
        return f"Psalm {self.psalm.number}: {self.number}"
