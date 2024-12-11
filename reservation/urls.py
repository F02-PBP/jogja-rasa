from django.urls import path
from reservation.views import show_reservation, delete_reservation, show_json_by_id, show_json, delete_reservation, edit_reservation
from reservation.views import create_reservation_flutter, delete_reservation_flutter, edit_reservation_flutter

app_name = 'reservation'

urlpatterns = [
    path('', show_reservation, name='show_reservation'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('json/', show_json, name='show_json'),
    path('delete/<str:id>/', delete_reservation, name='delete_reservation'),
    path('edit/<str:id>/', edit_reservation, name='edit_reservation'),
    path('create-reservation/', create_reservation_flutter, name='create_reservation_flutter'),
    path('delete-reservation/<str:id>/', delete_reservation_flutter, name='delete_reservation_flutter'),
    path('edit-reservation/<str:id>/', edit_reservation_flutter, name='edit_reservation_flutter'),
]