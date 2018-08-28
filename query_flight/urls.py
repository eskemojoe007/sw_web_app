from django.urls import path
from . import views
from . import apiviews
from rest_framework.routers import DefaultRouter

app_name = 'query_flight'

# Set up routers
router = DefaultRouter()
router.register('airports', apiviews.AirportViewSet, base_name='airports')
router.register('flights', apiviews.FlightViewSet, base_name='flights')
router.register('searchs', apiviews.SearchViewSet, base_name='searchs')
router.register('searchcards', apiviews.SearchCardViewSet, base_name='searchcards')


urlpatterns = [
    path('flights/<int:pk>/layovers/',
         apiviews.LayoverList.as_view(), name='layovers-list'),
    path('search/api/', apiviews.SearchPost.as_view(), name='search-post'),
    path('', views.index, name='index'),
    path('dummy', views.dummy, name='dummy'),
    # re_path(r'^(?i)airport/(?P<pk>[\w-]{3})/$',views.AirportView.as_view(),name='Airport'),
    # path('airport/<str:pk>/',views.AirportView.as_view(),name='Airport_Specific'),
    # path('airport/',views.AirportIndexView.as_view(),name='Airport'),
    # path('flight/new/',views.flight_new,name='New_Flight'),
    path('search/new/', views.search, name='search'),
]

urlpatterns += router.urls
