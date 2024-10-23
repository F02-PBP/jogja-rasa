from django.urls import path, include
from .views import register, login, show_landing_page, logout_user, search_restaurants

app_name = 'main'

urlpatterns = [
    path('', show_landing_page, name='show_landing_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('api/restaurants', search_restaurants, name='search_restaurants'),
    path('forum/', include('forum.urls', namespace='forum')),
]