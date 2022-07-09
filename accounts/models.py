from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **other_fields, ):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **other_fields, )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    objects = CustomUserManager()

    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username


class ActivateUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=300, blank=False, null=False)
    expiry = models.DateTimeField(blank=False, null=False)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.is_activated}"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_account")
    about = models.TextField(null=True, blank=True, max_length=500)
    profile_photo = ResizedImageField(size=[300, 250], default='default_profile_photo.jpg',
                                      upload_to='user_profile_photos',force_format='PNG')
    # profile_photo = models.ImageField(default='default_profile_photo.jpg',upload_to='user_profile_photos')
    role = models.CharField(max_length=255, default='Administrator')

    def save(self, *args, **kwargs):
        im = Image.open(self.profile_photo)
        im.convert('RGB')
        output = BytesIO()
        im = im.resize((200, 200))
        im.save(output, format='PNG', quality=100)
        output.seek(0)
        self.img = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.profile_photo.name.split('.')[0],
                                        'image/jpeg',
                                        sys.getsizeof(output), None)
        super().save()
        print("resized")

    @property
    def get_profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        else:
            return "/media/default_profile_photo.jpg"


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)