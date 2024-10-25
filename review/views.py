from django.shortcuts import render
from restaurants.models import Restaurant
from review.models import Review
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import datetime
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound
from restaurants.scripts import import_data
from main.models import UserProfile

@login_required(login_url='/login/')
def show_review(request):
    restaurants = Restaurant.objects.all()
    reviews = Review.objects.all()

    context = {
        'can_view_personalized_info': True,
        'can_manage_bookmarks': True,
        'can_rate_and_review': True,
        'can_manage_reservations': True,
        'can_participate_in_forum': True,
        'can_view_restaurants': True,
        'can_search_nearby': True,
        'can_view_reviews': True,
        'can_view_discussions': True,
        'restaurants': restaurants,
        'review': reviews,
    }

    return render(request, "review.html", context)

def calculate_rating(reviews):
    rating = visitor = 0
    for review in reviews:
        rating += review.rating
        visitor += 1
    if visitor > 0:
        rating /= visitor
    return [rating, visitor]


@login_required(login_url='/login/')
def show_review_more(request, id):

    restaurant = Restaurant.objects.get(pk=id)
    reviews = Review.objects.filter(restaurant=restaurant)
    users = UserProfile.objects.all()
    rating, visitor = calculate_rating(reviews)
    
    context = {
        'restaurant': restaurant,
        'rating': rating,
        'visitor': visitor,
        'reviews': serializers.serialize('json', Review.objects.filter(restaurant=restaurant)),
        'users': serializers.serialize('json', users),

    }
    return render(request, 'choose_restaurant.html', context)

@csrf_exempt
@require_POST
def create_review(request):
    resto_id = int(request.POST.get('pk_resto'))
    resto = Restaurant.objects.get(pk=resto_id)
    user = request.user
    date = datetime.now()
    rating = request.POST.get('rating')
    review = request.POST.get('review')
    new_review = Review(user=user, restaurant=resto, review=review, date=date, rating=rating)
    new_review.save()
    return HttpResponse(b"CREATED", status=201)
    
def show_restaurants_json(request):
    restaurants = Restaurant.objects.all()
    return HttpResponse(serializers.serialize('json', restaurants), content_type="application/json")

def show_reviews_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_reviews_by_restaurant_json(request, id):
    data = Review.objects.filter(restaurant=Restaurant.objects.get(pk=id))
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')