# Generated by Django 5.0.6 on 2024-06-12 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("studyPlans", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="Date",
            new_name="deadlines",
        ),
    ]
