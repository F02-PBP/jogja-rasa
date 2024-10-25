from django.urls import path
from .views import register, login, show_landing_page, logout_user, search_restaurants, rekomendasi_makanan, profile

app_name = 'main'

urlpatterns = [
    path('', show_landing_page, name='show_landing_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('search_restaurants/', search_restaurants, name='search_restaurants'),
    path('get_recommendations/', rekomendasi_makanan, name='get_recommendations'),
    path('profile/', profile, name='profile'),
]