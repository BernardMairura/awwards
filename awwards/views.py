from django.shortcuts import render,redirect,get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from .models import Project,Review,NewsLetterRecipients,Comments,Profile
from .forms import ProjectUploadForm, RegistrationForm,PostForm, NewsLetterForm,VotesForm,ReviewForm,ProfileEditForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.template.loader import render_to_string
from django.views.generic import RedirectView
from .serializer import ProfileSerializer,ProjectSerializer
from .permissions import IsAdminOrReadOnly



# Create your views here.


def home(request):
    projects = Project.objects.all()
    
    context = {
        'projects':projects,
    }
    return render(request,'index.html',context)

@login_required(login_url="/accounts/login/")    
def projects(request,project_id):
    try:
        projects = Project.objects.get(id=project_id)
        all = Review.objects.filter(project=project_id) 
        print(all)
    except Exception as e:
        raise Http404() 
    
    '''
    User count
    '''
    count = 0
    for i in all:
        count+=i.usability
        count+=i.design
        count+=i.content
    
    if count > 0:
        average = round(count/3,1)
    else:
        average = 0
        
    if request.method == 'POST':
        form = VotesForm(request.POST)
        print('from',form)
        if form.is_valid():
            
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project_id
           
            rate.save()
        return redirect('projects',project_id)
        
    else:
        form = VotesForm() 
        
    '''
    Rating and votes logic
    '''
    votes = Review.objects.filter(project=project_id)
    usability = []
    design = []
    content = [] 
    
    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content) 
    '''
    Len() used for finding no. of items in each rating category
    '''
    if len(usability) > 0 or len(design)>0 or len(content)>0:
        average_usability = round(sum(usability)/len(usability),1) 
        average_design = round(sum(design)/len(design),1)
        average_content = round(sum(content)/len(content),1) 
            
        average_rating = round((average_content+average_design+average_usability)/3,1) 
    
    else:
        average_content=0.0
        average_design=0.0
        average_usability=0.0
        average_rating = 0.0
        
    '''
    Logic for a vote per user
    '''
    
    arr1 = []
    for use in votes:
        arr1.append(use.user_id) 
                
    auth = arr1
       
    reviews = ReviewForm(request.POST)
    if request.method == 'POST':
        
        if reviews.is_valid():
            comment = reviews.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect ('projects',project_id)
        else:
            reviews = ReviewForm()
            
       
    context = {
        'projects':projects,
        'form':form,
        'usability':average_usability,
        'design':average_design,
        'content':average_content,
        'average_rating':average_rating,
        'auth':auth,
        'all':all,
        'average':average,
        'reviews':reviews,
        
    }
    
    return render(request,'post.html',context) 



@login_required(login_url="/accounts/login/")
def profile(request,username=None):
    profile= Profile.objects.get(user=username)
    print(profile)
    

    # obj = get_object_or_404(User, username=username)
    # user = obj.profile
    # context = {
    #     "object": obj,
    #     "user": user,
    # }

    current_user = request.user
    
    
    try:
        profile_details = Profile.get_by_id(user.id)
    except:
        profile_details = Profile.filter_by_id(user.id)
    projects = Project.get_profile_projects(user.id)
    
    return render(request, 'profile.html',{"profile":profile,"profile_details":profile_details,"projects":projects}) 


@login_required(login_url='accounts/login/')
def update_profile(request):
    title = "Update Profile"
    current_user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit=False)
            home.profile =current_user
            form.save()
        return redirect(profile)
    else:
        form = ProfileEditForm()
    context = {"current_user":current_user,"title":title,"form":form}
    return render(request, 'profile.html',context) 


@login_required(login_url="/accounts/login/")
def uploadproject(request):
  current_user = request.user
  if request.method == 'POST':
    form = ProjectUploadForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.profile = request.user
      project.save()
      return HttpResponseRedirect('index.html')
  else:
    form = ProjectUploadForm()
  context = {"form":form}
  return render(request,'uploads.html',context)

@login_required(login_url="/accounts/login/")
def search_results(request):
    if 'projects' in request.GET and request.GET['projects']:
        search_term = request.GET.get("projects")
        searched_projects = Project.search_by_projects(search_term)
    
    
        message = f'{search_term}'
    
        return render(request,'search.html',{"message":message,"projects":projects})

    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message,"projects":projects})


class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
'''
Using serializer for (GET) projects
'''
class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)















































# # details
# def details(request, slug):
#     project = Project.objects.get(slug=slug)
#     # getting the user reviews
#     reviews = Review.objects.filter(movie=movie)
#     context = {
#         'project': project,
#         'reviews': reviews,
#     }
#     return render(request, 'details.html', context)


#     # registering the user
# def register(request):
#     if request.user.is_authenticated:
#         return redirect("home")
#     else:
#         if request.method == 'POST':
#             form = RegistrationForm(request.POST or None)
#             if form.is_valid():
#                 form.save()
#                 return redirect("home")
#         else:
#             form = RegistrationForm(request.POST or None)
#         return render(request, 'register.html', {'form': form})

# # log in 
# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect("home")
#     else:
#         if request.method == 'POST':
#             # now we get the data from html templates
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             # authenticating the credentials
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 print("User is notNone") #meaning that the credentials are correct
#                 if user.is_active:
#                     login(request, user)
#                     return redirect("home")
#                 else:
#                     return render(request, 'login.html', {'error-message': 'Your account has been banned.'})
#             else:
#                 return render(request, 'login.html', {'error-message': 'Invalid Username or Password'})
#         return render(request, 'login.html')

# # logout
# def logout_user(request):
#     if request.user.is_authenticated:
#         logout(request)
#         return redirect("home")
#     else:
#         return redirect("login_user")


# #creating user profile
# def profile(request, user):
#     # get the contents by that user
#     username = User.objects.get(username=user)
    
#     reviews = Review.objects.filter(user=username)
#     context = {
#         'reviews':reviews,
#         'username': username
#     }
#     return render(request, 'profile.html', context)
    