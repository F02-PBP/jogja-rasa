from django.shortcuts import render
from .models import Restaurant
from django.http import JsonResponse

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
    }
    return render(request, 'main.html', context)

def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    data = [{
        'id': str(restaurant.id),
        'name': restaurant.name,
        'longitude': restaurant.longitude,
        'latitude': restaurant.latitude,
        'description': restaurant.description,
        'location': restaurant.get_location()
    } for restaurant in restaurants]
    return JsonResponse({'restaurants': data})

