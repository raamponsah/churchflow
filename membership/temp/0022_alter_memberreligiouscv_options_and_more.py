# Generated by Django 4.0.1 on 2022-01-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0021_welfaresupport_delete_trackdailyactivities_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memberreligiouscv',
            options={'verbose_name': 'Member Christian Information', 'verbose_name_plural': 'Members Christian Information'},
        ),
        migrations.AlterModelOptions(
            name='membershipmonthlylevy',
            options={'verbose_name': 'Membership Dues', 'verbose_name_plural': 'Membership Dues'},
        ),
        migrations.RemoveField(
            model_name='welfaresupport',
            name='amount_contributed',
        ),
        migrations.RemoveField(
            model_name='welfaresupport',
            name='members',
        ),
        migrations.AddField(
            model_name='member',
            name='welfare_contributions',
            field=models.ManyToManyField(blank=True, null=True, to='membership.WelfareSupport'),
        ),
    ]