from django.urls import path
from views import restaurant_list

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
]