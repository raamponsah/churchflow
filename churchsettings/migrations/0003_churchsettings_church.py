# Generated by Django 4.0.1 on 2022-04-23 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('churchsettings', '0002_churchsetup_description_churchsetup_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchsettings',
            name='church',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='churchsettings.churchsetup'),
            preserve_default=False,
        ),
    ]