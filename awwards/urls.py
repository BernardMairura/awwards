from django.urls import path,re_path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name='home'),
    re_path(r'^$',views.home,name='home'),
    re_path(r'^projects/(\d+)',views.projects,name='projects'),
    # path('profile/<int:user_id>/', views.profile, name='profile'),
    re_path(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
    re_path(r'^uploads/', views.uploadproject, name='uploadproject'),
    re_path(r'^search/', views.search_results, name='search_results'),
    re_path(r'^api/profiles/$', views.ProfileList.as_view(),name='profile_list'),
    re_path(r'^api/projects/$', views.ProjectList.as_view(),name='projects_list'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 