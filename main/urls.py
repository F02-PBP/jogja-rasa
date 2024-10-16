from django.urls import path
from .views import register, login, show_landing_page

app_name = 'main'

urlpatterns = [
    path('', show_landing_page, name='show_landing_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]