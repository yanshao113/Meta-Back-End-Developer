# Generated by Django 4.2.4 on 2023-08-25 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                ("name", models.CharField(max_length=255)),
                ("booking_date", models.DateField(default=datetime.date(2023, 8, 25))),
                ("no_of_guests", models.SmallIntegerField(default=6)),
            ],
        ),
        migrations.CreateModel(
            name="Menu",
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
                ("title", models.CharField(max_length=255)),
                (
                    "price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=10),
                ),
                ("inventory", models.SmallIntegerField(default=5)),
            ],
        ),
    ]