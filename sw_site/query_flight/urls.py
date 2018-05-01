from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^(?i)airport/(?P<pk>[\w-]{3})/$',views.AirportView.as_view(),name='Airport'),
    path('airport/<str:pk>/',views.AirportView.as_view(),name='Airport_Specific'),
    path('airport/',views.AirportIndexView.as_view(),name='Airport'),
    path('flight/new/',views.flight_new,name='New_Flight'),
    path('search/new/',views.search,name='search'),
]
