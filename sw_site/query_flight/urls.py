from django.urls import path, re_path
from . import views
from . import apiviews
from rest_framework.routers import DefaultRouter

app_name='query_flight'

#Set up routers
router = DefaultRouter()
router.register('airports',apiviews.AirportViewSet,base_name='airports')
router.register('flights',apiviews.FlightViewSet,base_name='flights')
router.register('searchs',apiviews.SearchViewSet,base_name='searchs')


urlpatterns = [
    path('flights/<int:pk>/layovers/',apiviews.LayoverList.as_view(),name='layovers-list'),
    path('', views.index, name='index'),
    # re_path(r'^(?i)airport/(?P<pk>[\w-]{3})/$',views.AirportView.as_view(),name='Airport'),
    # path('airport/<str:pk>/',views.AirportView.as_view(),name='Airport_Specific'),
    # path('airport/',views.AirportIndexView.as_view(),name='Airport'),
    # path('flight/new/',views.flight_new,name='New_Flight'),
    path('search/new/',views.search,name='search'),
]

urlpatterns += router.urls
