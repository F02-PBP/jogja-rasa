from django.shortcuts import render, redirect
from main.models import *
from restaurants.models import *
from reservation.models import Reservation
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder

def show_reservation(request):
    reservation_data = Reservation.objects.all()

    context = {
        'reservation_data': reservation_data,
    }
    return render(request, "reservation.html", context)

@csrf_exempt
def delete_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id)
        reservation.delete()
        return JsonResponse({'success': True, 'message': 'Reservation deleted successfully.'})
    except Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found.'})
    
@csrf_exempt
def edit_reservation(request, id):
    if request.method == 'POST':
        try:
            # Get product berdasarkan id
            reservation = Reservation.objects.get(pk=id)

            data = json.loads(request.body)  # Load the JSON data
            print(data)  # For debugging, log the entire data received

            date = data.get('date')
            print(date)  # Debugging output
            time = data.get('time')
            print(time)  # Debugging output
            number_of_people = data.get('number_of_people')
            print(number_of_people)  # Debugging output


            # Update the product fields
            if date:
                reservation.date = date
            if time:
                reservation.time = time
            if number_of_people:
                reservation.number_of_people = number_of_people

            # Save the updated product
            reservation.save()

            return JsonResponse({'success': True, 'message': 'Product updated successfully'})

        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})
    
def show_json_by_id(request, id):
    data = Reservation.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json(request):
    data = Reservation.objects.filter(user=request.user)
    reservation_data = []
    for resv in data:
        reservation_data.append({
            "pk": resv.pk,
            "fields" :{
                "reservation_id": resv.reservation_id,
                "user": resv.user.pk,
                "date": resv.date,
                "time": resv.time,
                "number_of_people": resv.number_of_people,
                "restaurant": {
                    "id": resv.restaurant.id,
                    "name": resv.restaurant.name,
                    "longitude": resv.restaurant.longitude,
                    "latitude": resv.restaurant.latitude,
                    "description": resv.restaurant.description
                }
            }
        })
    return JsonResponse(reservation_data, safe=False)