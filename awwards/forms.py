from django import forms
from .models import Project,Profile,Review,User,Comments
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea,ModelForm,IntegerField

# creating the forms
class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title','image','body', 'link')


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

class VotesForm(forms.ModelForm):
    '''
    Form for rating projects posted
    '''
    class Meta:
        model = Review
        fields = ('design','usability','content')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comments',)


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


