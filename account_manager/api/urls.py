from django.urls import path
from account_manager.api.views import api_signup
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', views.api_signup, name='api_signup'),
    path('login', obtain_auth_token, name='api_login'),
    path('properties', views.account_properties, name='api_properties'),
    path('properties/update', views.account_update, name='api_update'),
]
