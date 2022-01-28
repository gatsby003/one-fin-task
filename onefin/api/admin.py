from django.contrib import admin
from .models import Collection, AppUser

# Register your models here.

admin.site.register(AppUser)
admin.site.register(Collection)
