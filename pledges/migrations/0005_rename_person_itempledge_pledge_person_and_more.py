# Generated by Django 4.0.1 on 2022-04-11 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pledges', '0004_rename_pledge_person_itempledge_person_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itempledge',
            old_name='person',
            new_name='pledge_person',
        ),
        migrations.RenameField(
            model_name='monetarypledge',
            old_name='person',
            new_name='pledge_person',
        ),
        migrations.RemoveField(
            model_name='memberitempledge',
            name='person',
        ),
        migrations.RemoveField(
            model_name='membermonetarypledge',
            name='person',
        ),
    ]