from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('test/', views.test, name='test'),
    path('getitems/', views.get_items, name='get_items'),
    path('postitems/', views.post_items, name='post_items'),
    path('deleteitem/<int:item_id>/', views.delete_items, name='delete_items'),
    path('patchitem/<int:item_id>/', views.patch_item, name='patch_item'),
]
