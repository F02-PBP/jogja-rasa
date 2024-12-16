from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('toggle_bookmark_flutter/<str:restaurant_id>/', views.toggle_bookmark_flutter, name='toggle_bookmark_flutter'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('json/', views.show_json, name='show_json'),
    path('get_bookmarks_flutter/', views.get_bookmarks_flutter, name='get_bookmarks_flutter'),
]
