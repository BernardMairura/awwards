from django import forms
from .models import Project,UserProfile,Review
from django.contrib.auth.forms import UserCreationForm

# creating the forms
class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'released_date', 'director', 'cast', 'image',)
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
