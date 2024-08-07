# Generated by Django 5.0.7 on 2024-08-07 02:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Psalm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                ("title", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Verse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                ("first_half", models.TextField()),
                ("second_half", models.TextField()),
                (
                    "psalm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="psalter.psalm"
                    ),
                ),
            ],
        ),
    ]
