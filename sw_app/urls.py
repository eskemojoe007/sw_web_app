from django.urls import path
# from . import views
from .apiviews import RegistrationAPI, LoginAPI, UserAPI

app_name = 'sw_app'

urlpatterns = [
    path('auth/register/', RegistrationAPI.as_view(), name='user-register'),
    path('auth/login/', LoginAPI.as_view(), name='user-login'),
    path('auth/user/', LoginAPI.as_view(), name='user'),
]
