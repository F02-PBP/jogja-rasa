from django.shortcuts import render
from .models import Restaurant
from django.http import JsonResponse

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
    }
    return render(request, 'main.html', context)
