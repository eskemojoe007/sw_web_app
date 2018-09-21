from django.urls import path
# from . import views
from .apiviews import RegistrationAPI

app_name = 'sw_app'

urlpatterns = [
    path('auth/register/', RegistrationAPI.as_view(), name='user-post'),
]
