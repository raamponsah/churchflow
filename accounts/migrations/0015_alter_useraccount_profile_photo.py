# Generated by Django 4.0.1 on 2022-06-23 10:17

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_useraccount_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_photo',
            field=django_resized.forms.ResizedImageField(crop=None, default='default_profile_photo.jpg', force_format='PNG', keep_meta=True, quality=75, size=[300, 250], upload_to='user_profile_photos'),
        ),
    ]
