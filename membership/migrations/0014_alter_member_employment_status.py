# Generated by Django 4.0.1 on 2022-06-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0013_member_company_employed_member_employment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='employment_status',
            field=models.BooleanField(blank=True, choices=[('not-applicable', 'Not Applicable'), ('unemployed', 'Unemployed'), ('self-employed', 'Self-Employed'), ('employed', 'Employed')], default=False, null=True),
        ),
    ]
