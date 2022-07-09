import datetime

from PIL import Image
from django.db import models
from django_countries.fields import CountryField

from groups.models import Group

# Create your models here.

# from welfare.models import WelfareContribution
from membership.ChoiceDataSets.ChoiceSets import OCCUPATIONS, COUNTRIES

GENERIC_BOOLEAN = (
    (False, 'No'),
    (True, 'Yes'),
)


class Member(models.Model):
    EMPLOYMENT_STATUS_CHOICES = (
        ('not-applicable', 'Not Applicable'),
        ('unemployed', 'Unemployed'),
        ('self-employed', 'Self-Employed'),
        ('employed', 'Employed'),
    )

    SECTORS = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    EDUCATION_LEVEL = (
        ('no-school', 'Not Applicable'),
        ('primary', 'Primary'),
        ('jhs', 'JHS'),
        ('shs', 'SHS'),
        ('vocational', 'Vocational'),
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('diploma', 'Diploma'),
        ('hnd', 'HND'),
        ('degree', 'Degree'),
        ('masters', 'masters'),
        ('phd', 'PHD'),
    )

    GENDER_TYPE = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    LIVING_STATUS = (
        ('deceased', 'Deceased'),
        ('alive', 'Alive'),
    )

    RELATIONSHIP = (
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('son', 'Son'),
        ('cousin', 'Cousin'),
        ('friend', 'Friend'),
    )

    MARITAL_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('co-habitating', 'Co-habitating'),
        ('engaged', 'Engaged'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('religious', 'religious'),
    )

    muid = models.CharField(max_length=12, blank=False, null=False, editable=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=255, null=False, blank=False, default=None, choices=GENDER_TYPE)
    email = models.EmailField(max_length=255, blank=True, null=True, db_index=True, unique=True, default=None)
    date_of_birth = models.DateField(blank=False, null=False, default=None)
    primary_phone = models.CharField(max_length=255, blank=False, null=False)
    secondary_phone = models.CharField(max_length=255, blank=True, null=True, default=None)
    country = models.CharField(max_length=255, blank=False, null=False, default=None, choices=COUNTRIES)
    residential_address = models.CharField(max_length=255, blank=True, null=True)
    city_or_town = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=False, null=False, default=None)
    occupation = models.CharField(max_length=255, blank=False, null=False, choices=OCCUPATIONS, default=None)
    employment_status = models.CharField(max_length=255,default=None, blank=True, null=True, choices=EMPLOYMENT_STATUS_CHOICES)
    company_employed = models.CharField(max_length=255, blank=True, null=True, default=None)
    sector = models.CharField(max_length=255, blank=False, null=False, choices=SECTORS, default=None)
    education_level = models.CharField(max_length=255, blank=False, null=False, choices=EDUCATION_LEVEL, default=None)
    marital_status = models.CharField(max_length=20, blank=False, null=False,
                                      choices=MARITAL_STATUS_CHOICES, default=MARITAL_STATUS_CHOICES[0])

    # family data 
    father_name = models.CharField(max_length=255, blank=False, null=False, default=None)
    father_hometown = models.CharField(max_length=255, blank=False, null=False, default=None)
    father_living_status = models.CharField(max_length=255, null=False, blank=False, default=None,
                                            choices=LIVING_STATUS)
    mother_name = models.CharField(max_length=255, blank=False, null=False, default=None)
    mother_hometown = models.CharField(max_length=255, blank=False, null=False, default=None)
    mother_living_status = models.CharField(max_length=255, null=False, blank=False, default=None,
                                            choices=LIVING_STATUS)
    # next of kin
    next_of_kin_name = models.CharField(max_length=255, blank=False, null=False, default=None)
    next_of_kin_relationship = models.CharField(max_length=255, blank=False, null=False, choices=RELATIONSHIP,
                                                default=None)
    next_of_kin_primary_phone = models.CharField(max_length=255, blank=False, null=False, default=None)
    next_of_kin_email = models.EmailField(max_length=255, blank=True, null=True, default=None)
    next_of_kin_location = models.CharField(max_length=255, blank=True, null=False, default=None)

    # emergency contact
    emergency_name = models.CharField(max_length=255, blank=False, null=False, default=None)
    emergency_primary_phone = models.CharField(max_length=255, blank=False, null=False, default=None)

    # organisation
    organisations = models.ManyToManyField(Group, blank=True, related_name='groups')
    profile_photo = models.ImageField(default='default_profile_photo.jpg', blank=True, null=True,
                                      upload_to='profile_photos')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def get_profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        else:
            return "/media/default_profile_photo.jpg"

    def save(self, *args, **kwargs):
        try:
            super().save()

            profile_photo = Image.open(self.profile_photo.path)  # Open image
            # resize image
            if profile_photo.height > 150 or profile_photo.width > 150:
                output_size = (150, 150)
                profile_photo.thumbnail(output_size)  # Resize image
                profile_photo.save(self.profile_photo.path)  # Save it again and override the larger image
        except:
            pass

    def save(self, *args, **kwargs):
        self.muid = f"{self.last_name[-2:].upper()}{self.first_name[-2:].upper()}{str(self.date_of_birth)[:4]}{self.id}"
        super().save()

    @property
    def fullname(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"


class MemberReligiousCV(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="member_ccv")

    #    baptism_cv
    baptism_status = models.BooleanField(default=False, blank=True, null=True, choices=GENERIC_BOOLEAN)
    baptism_date = models.DateField(null=True, blank=True)
    baptism_location = models.CharField(max_length=255, blank=True, null=True)
    baptised_by = models.CharField(max_length=255, blank=True, null=True)

    #    holy_communion_cv
    holy_communion_status = models.BooleanField(default=False, blank=True, null=True, choices=GENERIC_BOOLEAN)
    holy_communion_date = models.DateField(null=True, blank=True)
    holy_communion_location = models.CharField(max_length=255, blank=True, null=True)
    holy_communion_given_by = models.CharField(max_length=255, blank=True, null=True)

    #    confirmation_cv
    confirmation_status = models.BooleanField(default=False, blank=True, null=True, choices=GENERIC_BOOLEAN)
    confirmation_date = models.DateField(null=True, blank=True)
    confirmation_location = models.CharField(max_length=255, blank=True, null=True)
    confirmed_by = models.CharField(max_length=255, blank=True, null=True)

    #    holy_matrimony_cv
    holy_matrimony_status = models.BooleanField(default=False, blank=True, null=True, choices=GENERIC_BOOLEAN)
    holy_matrimony_date = models.DateField(null=True, blank=True)
    holy_matrimony_location = models.CharField(max_length=255, blank=True, null=True)
    holy_matrimony_presided_by = models.CharField(max_length=255, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Member Christian Information'
        verbose_name_plural = 'Members Christian Information'