from django.urls import path
from . import views

app_name = 'weatherapi'

urlpatterns = [
    path('greeting', views.hello, name='greeting'),
    path('hello', views.get_client_info, name='hello')
]
