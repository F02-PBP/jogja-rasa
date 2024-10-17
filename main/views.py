from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from restaurants.models import Restaurant
from django.http import JsonResponse
from django.db.models import Q
from geopy.distance import geodesic
import csv

# ini bisa diganti bebas ya
def show_landing_page(request):
    restaurants = Restaurant.objects.all()
    context = {
        'can_view_restaurants': True,
        'can_search_nearby': True,
        'can_view_reviews': True,
        'can_view_discussions': True,
        'restaurants': restaurants,
    }
    if request.user.is_authenticated:
        context.update({
            'can_view_personalized_info': True,
            'can_manage_bookmarks': True,
            'can_rate_and_review': True,
            'can_manage_reservations': True,
            'can_participate_in_forum': True,
        })
    return render(request, 'main.html', context)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('main:show_landing_page') 
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('main:show_landing_page') 
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('main:show_landing_page') 

def search_restaurants(request):
    query = request.GET.get('query', '')
    food_type = request.GET.get('food_type', '')
    area = request.GET.get('area', '')
    nearby = request.GET.get('nearby', 'false').lower() == 'true'

    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if food_type:
        restaurants = restaurants.filter(name__icontains=food_type)

    if area and nearby:
        center_lat, center_lon = get_area_center(area)
        if center_lat and center_lon:
            restaurants = [
                r for r in restaurants
                if geodesic((center_lat, center_lon), (r.latitude, r.longitude)).km <= 5
            ]

    data = [
        {
            'name': r.name,
            'description': r.description,
            'latitude': r.latitude,
            'longitude': r.longitude,
            'distance': geodesic((center_lat, center_lon), (r.latitude, r.longitude)).km if area and nearby else None
        }
        for r in restaurants
    ]

    return JsonResponse(data, safe=False)

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

def get_area_center(area):
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Nama Tempat Makan'] == area:
                return float(row['Latitude']), float(row['Longitude'])
    return None