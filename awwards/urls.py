from django.urls import path,re_path
from .import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.login_user, name='login_user'),
    re_path(r'^logout/$', views.logout_user, name='logout_user'),
    re_path(r'^profile/(?P<user>[.\-\w]+)/$', views.profile, name='profile')

]