from django.urls import path
from reservation.views import show_reservation, delete_reservation, show_json_by_id, show_json, delete_reservation, edit_reservation

app_name = 'reservation'

urlpatterns = [
    path('', show_reservation, name='show_reservation'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('json/', show_json, name='show_json'),
    path('delete/<str:id>/', delete_reservation, name='delete_reservation'),
    path('edit/<str:id>/', edit_reservation, name='edit_reservation'),

]