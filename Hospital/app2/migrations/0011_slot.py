# Generated by Django 5.0.6 on 2024-06-21 06:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app2", "0010_patientt_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Slot",
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
                ("day", models.CharField(max_length=20)),
                ("time_slot", models.CharField(max_length=10)),
                ("capacity", models.IntegerField()),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app2.addstaff"
                    ),
                ),
            ],
        ),
    ]
