# Generated by Django 4.0.1 on 2022-01-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_remove_churchorganisation_president'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchorganisation',
            name='organisation_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]