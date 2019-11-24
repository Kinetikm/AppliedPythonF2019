from django.conf.urls import url
import django.contrib.auth.views
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
