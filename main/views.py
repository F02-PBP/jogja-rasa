from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from restaurants.models import Restaurant

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