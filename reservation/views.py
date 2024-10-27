from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from main.models import *
from restaurants.models import *
from reservation.models import Reservation
import json

@login_required
def show_reservation(request):
    reservation_data = Reservation.objects.filter(user=request.user)
    context = {
        'reservation_data': reservation_data,
    }
    return render(request, "reservation.html", context)

@csrf_exempt
@login_required
def delete_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id, user=request.user)
        reservation.delete()
        return JsonResponse({
            'success': True, 
            'message': 'Reservation deleted successfully.'
        })
    except Reservation.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Reservation not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=500)

@csrf_exempt
@login_required
def edit_reservation(request, id):
    if request.method == 'POST':
        try:
            reservation = Reservation.objects.get(pk=id, user=request.user)
            
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                }, status=400)

            print(f"Received data: {data}")
            if 'date' in data:
                reservation.date = data['date']
            if 'time' in data:
                reservation.time = data['time']
            if 'number_of_people' in data:
                reservation.number_of_people = data['number_of_people']

            reservation.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Reservation updated successfully',
                'data': {
                    'id': str(reservation.id),
                    'date': reservation.date,
                    'time': str(reservation.time),
                    'number_of_people': reservation.number_of_people
                }
            })
            
        except Reservation.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Reservation not found'
            }, status=404)
        except Exception as e:
            print(f"Error updating reservation: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error updating reservation: {str(e)}'
            }, status=500)
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

@login_required
def show_json_by_id(request, id):
    try:
        data = Reservation.objects.filter(pk=id, user=request.user)
        if not data.exists():
            return JsonResponse({
                'success': False,
                'message': 'Reservation not found'
            }, status=404)
        return HttpResponse(
            serializers.serialize("json", data),
            content_type="application/json"
        )
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@login_required
def show_json(request):
    try:
        data = Reservation.objects.filter(user=request.user)
        reservation_data = []
        
        for resv in data:
            reservation_data.append({
                "pk": str(resv.id),  
                "fields": {
                    "reservation_id": str(resv.id), 
                    "user": resv.user.pk,
                    "date": resv.date.strftime('%Y-%m-%d'),  
                    "time": resv.time.strftime('%H:%M'),  
                    "number_of_people": resv.number_of_people,
                    "restaurant": {
                        "id": str(resv.restaurant.id),
                        "name": resv.restaurant.name,
                        "longitude": resv.restaurant.longitude,
                        "latitude": resv.restaurant.latitude,
                        "description": resv.restaurant.description
                    }
                }
            })
        
        return JsonResponse(reservation_data, safe=False)
        
    except Exception as e:
        print(f"Error in show_json: {str(e)}") 
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
