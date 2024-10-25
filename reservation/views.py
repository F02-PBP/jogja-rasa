from django.shortcuts import render, redirect
from main.models import *
from reservation.models import Reservation
from reservation.forms import ReservationForm

def show_reservation(request):
    reservation_data = Reservation.objects.all()

    context = {
        'reservation_data': reservation_data,
    }
    return render(request, "reservation.html", context)