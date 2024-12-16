from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    interested_food = [
        ("soto", "Soto"),
        ("gudeg", "Gudeg"),
        ("bakpia", "Bakpia"),
        ("sate", "Sate"),
        ("nasi goreng", "Nasi Goreng"),
        ("olahan ayam", "Olahan Ayam"),
        ("olahan ikan", "Olahan Ikan"),
        ("olahan mie", "Olahan Mie"),
        ("kopi", "Kopi"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    interested_in = models.CharField(max_length=50, choices=interested_food, default="Pilih Makanan Favorit", blank=False)
    # interested_in = "soto"