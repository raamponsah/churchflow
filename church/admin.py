from django.contrib import admin

# Register your models here.
from church.models import ChurchSettings, Church

admin.site.register(Church)
admin.site.register(ChurchSettings)