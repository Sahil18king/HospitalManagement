# Generated by Django 5.0.6 on 2024-06-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="userr",
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
                ("username", models.CharField(max_length=20)),
                ("fname", models.CharField(max_length=20)),
                ("lname", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
        ),
    ]
