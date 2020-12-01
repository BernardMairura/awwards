
from rest_framework import serializers
from .models import Profile,Project

'''
Serializer classes for profile and projects [API]
Feature E: API endpoints
'''

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user','user_image','bio') 
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title','image','body','link')