from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project,Review
from .forms import ProjectAddForm, RegistrationForm,PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def home(request):
    # getting objects from the database
    projet = Project.objects.all()

    # search query
    # query = request.GET.get('q')
    # if query:
    #     projects = Project.objects.filter(title__icontains=query)

    # context = {
    #     'projects':projects
    # }
    return render(request, 'index.html')
    