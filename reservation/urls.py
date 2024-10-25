from django.urls import path
from reservation.views import show_reservation

app_name = 'reservation'

urlpatterns = [
    path('', show_reservation, name='show_reservation'),
]