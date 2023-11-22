# Generated by Django 4.2.7 on 2023-11-20 17:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0005_pitch_pitch_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pitch",
            old_name="kind",
            new_name="pitch_type",
        ),
        migrations.RemoveField(
            model_name="pitch",
            name="game",
        ),
        migrations.RemoveField(
            model_name="pitch",
            name="timestamp",
        ),
    ]