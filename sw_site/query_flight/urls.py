from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?i)airport/(?P<airport_id>[\w-]{3})/$',views.airport,name='Airport')
    # path('<str:airport_id>',views.airport,name='Airport')
]
