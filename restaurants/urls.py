from django.urls import path
from .views import restaurant_list, get_restaurants

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
    path('get_restaurants/', get_restaurants, name='get_restaurants'),
]