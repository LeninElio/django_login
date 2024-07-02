from django.urls import path
from . import views
from .views import openid_configuration


name = 'userlogin'
urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('.well-known/openid-configuration', openid_configuration, name='openid-configuration'),
    path('jwks/', views.jwks, name='jwks'),
]
