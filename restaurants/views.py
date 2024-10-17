from django.shortcuts import render
from .models import Restaurant

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    
    debug_info = {
        'database_connection': 'Connected',
        'model_fields': [field.name for field in Restaurant._meta.get_fields()],
        'test_restaurant': Restaurant.objects.first(),
        'restaurant_count': Restaurant.objects.count(),
    }
    
    context = {
        'restaurants': restaurants,
        'debug_info': debug_info,
    }
    
    return render(request, 'main.html', context)