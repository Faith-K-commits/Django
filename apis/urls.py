from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('test/', views.test, name='test'),
    path('getitems/', views.get_items, name='get_items'),
]
