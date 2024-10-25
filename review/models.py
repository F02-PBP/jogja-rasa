from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True)
    rating = models.IntegerField()
    review = models.CharField(max_length=100)