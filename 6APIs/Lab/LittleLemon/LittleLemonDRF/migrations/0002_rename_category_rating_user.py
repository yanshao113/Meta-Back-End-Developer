# Generated by Django 4.1.3 on 2023-08-17 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonDRF", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rating",
            old_name="category",
            new_name="user",
        ),
    ]
