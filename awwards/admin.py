from django.contrib import admin
from .models import Profile,User,Review,Project,Comments

# Register your models here.
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Project)
admin.site.register(Comments)