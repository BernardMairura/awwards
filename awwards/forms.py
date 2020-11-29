from django import forms
from .models import Project,UserProfile,Review,User
from django.contrib.auth.forms import UserCreationForm

# creating the forms
class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'image', 'body')
# creating form for creating users

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# review form
class PostForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review', 'rating')
