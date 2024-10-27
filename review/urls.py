from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns =[
    path('',show_review, name='show_review'),
    path('show_restaurants_json/', show_restaurants_json, name='show_restaurants_json'),
    path('show_reviews_json/', show_reviews_json, name='show_reviews_json'),
    path('create_review/', create_review, name='create_review'),
    path('show_review/<uuid:id>/', show_review_more, name='show_review_more'),
    path('show_reviews_by_restaurant_json/<uuid:id>/', show_reviews_by_restaurant_json, name='show_reviews_by_restaurant_json'),
    path('delete_review/<int:id>/', delete_review)
]