# Generated by Django 4.2.6 on 2023-10-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitchingdata',
            name='team',
            field=models.CharField(default='Bloomsberg', max_length=100),
            preserve_default=False,
        ),
    ]