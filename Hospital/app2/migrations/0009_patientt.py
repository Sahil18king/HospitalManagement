# Generated by Django 5.0.6 on 2024-06-20 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app2", "0008_remove_scheduled_allergies_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patientt",
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
                ("username", models.CharField(blank=True, max_length=150)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("blood_pressure", models.CharField(blank=True, max_length=50)),
                ("sugar_level", models.CharField(blank=True, max_length=50)),
                ("blood_group", models.CharField(blank=True, max_length=10)),
                ("gender", models.CharField(blank=True, max_length=10)),
                ("phone_number", models.CharField(blank=True, max_length=20)),
                ("weight", models.CharField(blank=True, max_length=10)),
                ("height", models.CharField(blank=True, max_length=10)),
                ("smoking_status", models.CharField(blank=True, max_length=20)),
                ("alcohol_use", models.CharField(blank=True, max_length=20)),
                ("has_insurance", models.CharField(blank=True, max_length=3)),
            ],
        ),
    ]
