from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('hello', views.hello, name='hello'),
]
