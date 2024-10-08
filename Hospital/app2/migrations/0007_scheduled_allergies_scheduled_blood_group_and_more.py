# Generated by Django 5.0.6 on 2024-06-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app2", "0006_scheduled_date_scheduled_time_slot"),
    ]

    operations = [
        migrations.AddField(
            model_name="scheduled",
            name="allergies",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scheduled",
            name="blood_group",
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scheduled",
            name="current_medication",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scheduled",
            name="gender",
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
