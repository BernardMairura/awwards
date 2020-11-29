from django.urls import path,re_path
from .import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    # re_path(r'^profile/(?P<user>[.\-\w]+)/$', views.profile, name='profile')

]