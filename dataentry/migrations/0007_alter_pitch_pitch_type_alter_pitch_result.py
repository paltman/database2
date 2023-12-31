# Generated by Django 4.2.7 on 2023-11-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0006_rename_kind_pitch_pitch_type_remove_pitch_game_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pitch",
            name="pitch_type",
            field=models.CharField(
                choices=[
                    ("FB", "Fastball"),
                    ("CB", "Curveball"),
                    ("CH", "Changeup"),
                    ("SL", "Slider"),
                    ("SPL", "Splitter"),
                    ("CUT", "Cutter"),
                    ("KN", "Knuck"),
                    ("EE", "Eephus"),
                ],
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="pitch",
            name="result",
            field=models.CharField(
                choices=[
                    ("BALL", "Ball"),
                    ("K Looking", "Strike Looking"),
                    ("K Swinging", "Strike Swinging"),
                    ("FB", "Foul Ball"),
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
