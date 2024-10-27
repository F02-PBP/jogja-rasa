from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from restaurants.models import Restaurant
from django.http import JsonResponse
from django.db.models import Q
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from reservation.models import Reservation
from django.http import HttpResponse
from django.core import serializers
from bookmarks.models import Bookmark

def home(request):
    return render(request, 'home.html')

def show_landing_page(request):
    restaurants = Restaurant.objects.all()
    recommended_restaurants = []
    user_bookmarks = []

    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            interested_food = user_profile.interested_in
            
            food_type_keywords = {
                'soto': ['soto', 'saoto'],
                'gudeg': ['gudeg'],
                'bakpia': ['bakpia', 'bakphia'],
                'sate': ['sate', 'satay'],
                'nasi goreng': ['nasi goreng', 'nasgor'],
                'olahan ayam': ['ayam', 'chicken', 'angkringan', 'oseng', 'sego koyor'],
                'olahan ikan': ['lele', 'mangut', 'teri', 'udang', 'kepala ikan'],
                'olahan mie': ['mie', 'bakmi'],
                'kopi': ['kopi', 'coffee'],
                'pencuci_mulut': ['es campur', 'es buah', 'es duren', 'pukis', 'es krim', 'rujak', 'ronde', 'lupis', 'jamu', 'hidangan tahu', 'lapis legit', 'martabak'],
                'olahan_daging': ['kambing', 'sapi', 'steak', 'burger', 'entok', 'empal'],
            }
            
            keywords = food_type_keywords.get(interested_food, [])
            if keywords:
                keyword_queries = Q()
                for keyword in keywords:
                    keyword_queries |= (
                        Q(name__icontains=keyword) |
                        Q(description__icontains=keyword)
                    )
                recommended_restaurants = Restaurant.objects.filter(keyword_queries)[:3]

            user_bookmarks = Bookmark.objects.filter(user=request.user).values_list('restaurant_id', flat=True)

        except Exception as e:
            print(f"Error getting recommendations: {e}")
            recommended_restaurants = []
    
    for restaurant in restaurants:
        restaurant.is_bookmarked = restaurant.id in user_bookmarks
    
    for restaurant in recommended_restaurants:
        restaurant.is_bookmarked = restaurant.id in user_bookmarks
    
    context = {
        'restaurants': restaurants,
        'recommended_restaurants': recommended_restaurants,
    }
    return render(request, 'main.html', context)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat. Silakan login.')
            return redirect('main:home') 
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan coba lagi.')
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
            messages.success(request, 'Anda berhasil login.')
            return redirect('main:home') 
        else:
            messages.error(request, 'Email atau password salah. Silakan coba lagi.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('main:home') 

def search_restaurants(request):
    query = request.GET.get('query', '').strip()
    region = request.GET.get('region', '').strip()
    food_type = request.GET.get('food_type', '').strip()
    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if food_type:
        food_type_keywords = {
            'soto': ['soto', 'saoto'],
            'gudeg': ['gudeg'],
            'bakpia': ['bakpia', 'bakphia'],
            'sate': ['sate', 'satay'],
            'nasi goreng': ['nasi goreng', 'nasgor'],
            'olahan ayam': ['ayam', 'chicken', 'angkringan', 'oseng', 'sego koyor'],
            'olahan ikan': ['lele', 'mangut', 'teri', 'udang', 'kepala ikan'],
            'olahan mie': ['mie', 'bakmi'],
            'kopi': ['kopi', 'coffee'],
            'pencuci_mulut': ['es campur', 'es buah', 'es duren', 'pukis', 'es krim', 'rujak', 'ronde', 'lupis', 'jamu', 'hidangan tahu', 'lapis legit', 'martabak'],
            'olahan_daging': ['kambing', 'sapi' 'steak', 'burger', 'entok', 'empal'],
        }
        
        keywords = food_type_keywords.get(food_type, [])
        if keywords:
            keyword_queries = Q()
            for keyword in keywords:
                keyword_queries |= (
                    Q(name__icontains=keyword) |
                    Q(description__icontains=keyword)
                )
            restaurants = restaurants.filter(keyword_queries)

    if region:
        region_display = region.replace('-', ' ').title()
        filtered_restaurants = [
            r for r in restaurants
            if r.get_location().lower() == region_display.lower()
        ]
        restaurants = filtered_restaurants

    if request.user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(user=request.user).values_list('restaurant_id', flat=True)
    else:
        user_bookmarks = []

    results = [{
        'id': restaurant.id,
        'name': restaurant.name,
        'description': restaurant.description,
        'location': restaurant.get_location(),
        'longitude': restaurant.longitude,
        'latitude': restaurant.latitude,
        'is_bookmarked': restaurant.id in user_bookmarks
    } for restaurant in restaurants]

    return JsonResponse({'results': results})

def rekomendasi_makanan(request):
    if not request.user.is_authenticated:
        return JsonResponse({'results': []})
    
    try:
        user_profile = request.user.userprofile
        interested_food = user_profile.interested_in
        food_display = dict(UserProfile.FOOD_CHOICES)[interested_food]

        food_type_keywords = {
            'soto': ['soto', 'saoto'],
            'gudeg': ['gudeg'],
            'bakpia': ['bakpia', 'bakphia'],
            'sate': ['sate', 'satay'],
            'nasi goreng': ['nasi goreng', 'nasgor'], 
            'olahan ayam': ['ayam', 'chicken', 'angkringan', 'oseng', 'sego koyor'],
            'olahan ikan': ['lele', 'mangut', 'teri', 'udang', 'kepala ikan'],
            'olahan mie': ['mie', 'bakmi'],
            'kopi': ['kopi', 'coffee'],
            'pencuci_mulut': ['es campur', 'es buah', 'es duren', 'pukis', 'es krim', 'rujak', 'ronde', 'lupis', 'jamu', 'hidangan tahu', 'lapis legit', 'martabak'],
            'olahan_daging': ['kambing', 'sapi', 'steak', 'burger', 'entok', 'empal'],
        }

        keywords = food_type_keywords.get(interested_food, [])

        if keywords:
            keyword_queries = Q()
            for keyword in keywords:
                keyword_queries |= (
                    Q(name__icontains=keyword) |
                    Q(description__icontains=keyword)
                )
            recommended_restaurants = Restaurant.objects.filter(keyword_queries)[:3]
            
            recommendations = [{
                'id': restaurant.id,
                'name': restaurant.name,
                'description': restaurant.description,
                'location': restaurant.get_location(),
                'longitude': restaurant.longitude,
                'latitude': restaurant.latitude
            } for restaurant in recommended_restaurants]
            
            return JsonResponse({
                'recommendations': recommendations,
                'interested_food': food_display
            })
        
        return JsonResponse({'recommendations': []})
    except Exception as e:
        print(f"Error in get_recommendations: {e}") 
        return JsonResponse({'recommendations': []})
    

@login_required
def profile(request):
    return render(request, 'profile.html')

def show_json(request):
    data = Restaurant.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_reservation(request):
    date = request.POST.get("date")
    time = request.POST.get("time")
    number_of_people = request.POST.get("number_of_people")
    user = request.user
    restaurant_id = request.POST.get("restaurantObj")

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)  
    except Restaurant.DoesNotExist:
        return HttpResponse(b"Restaurant not found", status=404)
    
    new_reservation = Reservation(
        date=date, time=time,
        number_of_people=number_of_people,
        user=user, restaurant=restaurant,
    )
    new_reservation.save()

    return HttpResponse(b"CREATED", status=201)
