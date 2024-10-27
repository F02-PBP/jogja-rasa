from django.urls import path
from .views import register, login, show_landing_page, logout_user, search_restaurants, rekomendasi_makanan, profile, home, add_reservation,show_json, show_json_by_id
from bookmarks import views
app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('cari-resto/', show_landing_page, name='cari-resto'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('search_restaurants/', search_restaurants, name='search_restaurants'),
    path('get_recommendations/', rekomendasi_makanan, name='get_recommendations'),
    path('profile/', profile, name='profile'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add_reservation/', add_reservation, name='add_reservation'),
    path('bookmark/', views.bookmark_list, name='bookmark_list'),
    path('toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
]