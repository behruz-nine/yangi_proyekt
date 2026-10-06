from django.contrib import admin
from .models import CustomUser, Verify

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Verify)
