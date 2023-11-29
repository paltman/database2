# Generated by Django 4.2.7 on 2023-11-29 00:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0008_customuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pitch",
            name="result",
            field=models.CharField(
                choices=[
                    ("BALL", "Ball"),
                    ("K Looking", "Strike Looking"),
                    ("K Swinging", "Strike Swinging"),
                    ("Foul Ball", "Foul Ball"),
                    ("BIP OUT", "BIP Out"),
                    ("SGL", "Single"),
                    ("DBL", "Double"),
                    ("TPL", "Triple"),
                    ("HR", "HR"),
                    ("HBP", "HBP"),
                    ("D3S", "Drop 3d & Safe"),
                    ("ROE", "Reach on Error"),
                ],
                max_length=100,
            ),
        ),
    ]
