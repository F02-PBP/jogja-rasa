import random
import string
from main.models import *

# Membuat string random dengan kombinasi huruf dan angka sepanjang 5 karakter
def generate_reservation_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
class Reservation(models.Model):
    reservation_id = models.CharField(max_length=5, unique=True, editable=False, default=generate_reservation_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()