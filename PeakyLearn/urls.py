from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),



]