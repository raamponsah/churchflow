# Generated by Django 4.0.1 on 2022-01-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pledges', '0008_alter_membermonetarypledge_amount_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialpledge',
            name='redeemed_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='membermaterialpledge',
            name='redeemed_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='membermonetarypledge',
            name='redeemed_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='monetarypledge',
            name='redeemed_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=255),
        ),
    ]
