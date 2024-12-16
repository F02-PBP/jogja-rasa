import datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from main.models import *
from restaurants.models import *
from reservation.models import Reservation, Restaurant
from reservation.models import Reservation, Restaurant
import json
import uuid
import logging

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

            # print(f"Received data: {data}")
            # print(f"Received data: {data}")
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

logger = logging.getLogger(__name__)
@csrf_exempt
def create_reservation_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reservation_id = str(uuid.uuid4())
            reservation_date = datetime.strptime(data["date"], "%Y-%m-%d") 
            reservation_time = datetime.strptime(data["time"], "%H:%M").time()
            restaurant_instance = Restaurant.objects.get(id=data["restaurant"]["id"])

            new_reservation = Reservation.objects.create(
                id=reservation_id,
                user=request.user,
                date=reservation_date,
                time=reservation_time,
                number_of_people=data["number_of_people"],
                restaurant=restaurant_instance
            )

            # Save the new reservation
            new_reservation.save()

            # Respond with success
            return JsonResponse({"status": "success", "reservation_id": reservation_id}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Restaurant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)
        except Exception as e:
            logger.error(f"Error creating reservation: {e}", exc_info=True)
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # Handle non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_reservation_flutter(request, id):
    if request.method == 'DELETE':
        try:
            # Try to convert the ID to a UUID
            reservation_id = uuid.UUID(id)
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()
            return HttpResponse("Reservation deleted successfully.")
        
        except ValueError as e:
            # If ID is not a valid UUID
            print(f"Invalid UUID format: {id}")
            return HttpResponse("Invalid reservation ID format.", status=400)

@csrf_exempt
def edit_reservation_flutter(request, id):
    if request.method == 'PUT':
        try:
            reservation_id = uuid.UUID(id)
            reservation = get_object_or_404(Reservation, id=reservation_id)

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                }, status=400)
            
            # Update fields in the request data
            if 'date' in data:
                reservation.date = data['date']
            if 'time' in data:
                reservation.time = data['time']
            if 'number_of_people' in data:
                reservation.number_of_people = data['number_of_people']

            reservation.save()

            return JsonResponse({
                'success': True,
                'message': 'Reservation updated successfully'
            }, status=200)

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
        'message': 'Invalid HTTP method'
    }, status=405)
