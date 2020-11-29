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


    # registering the user
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = RegistrationForm(request.POST or None)
        return render(request, 'register.html', {'form': form})

# log in 
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            # now we get the data from html templates
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticating the credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                print("User is notNone") #meaning that the credentials are correct
                if user.is_active:
                    login(request, user)
                    return redirect("home")
                else:
                    return render(request, 'login.html', {'error-message': 'Your account has been banned.'})
            else:
                return render(request, 'login.html', {'error-message': 'Invalid Username or Password'})
        return render(request, 'login.html')

# logout
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    else:
        return redirect("login_user")


#creating user profile
def profile(request, user):
    # get the contents by that user
    username = User.objects.get(username=user)
    
    reviews = Review.objects.filter(user=username)
    context = {
        'reviews':reviews,
        'username': username
    }
    return render(request, 'profile.html', context)
    