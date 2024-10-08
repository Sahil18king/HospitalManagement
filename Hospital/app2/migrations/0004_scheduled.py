# Generated by Django 5.0.6 on 2024-06-19 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app2", "0003_alter_addstaff_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="scheduled",
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
                ("department", models.CharField(max_length=20)),
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=10)),
                ("symptoms", models.CharField(max_length=200)),
                ("doctoremail", models.CharField(max_length=50)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app2.addstaff"
                    ),
                ),
            ],
        ),
    ]
