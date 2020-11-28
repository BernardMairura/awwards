from django.contrib import admin
from .models import UserProfile,User,Review

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Review)