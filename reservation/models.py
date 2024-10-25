import random
import string
from main.models import *
from restaurants.models import Restaurant

# Membuat string random dengan kombinasi huruf dan angka sepanjang 5 karakter
def generate_reservation_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
class Reservation(models.Model):
    PEOPLE_CHOICES = [
        (1, '1 orang'),
        (2, '2 orang'),
        (3, '3 orang'),
        (4, '4 orang'),
        (5, '5 orang'),
        (6, '6 orang'),
        (7, '7 orang'),
        (8, '8 orang'),
    ]

    reservation_id = models.CharField(max_length=5, unique=True, editable=False, default=generate_reservation_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveSmallIntegerField(choices=PEOPLE_CHOICES)