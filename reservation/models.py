import uuid
from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant

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

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='reservation_id'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveSmallIntegerField(choices=PEOPLE_CHOICES)

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username} at {self.restaurant.name}"

    class Meta:
        ordering = ['date', 'time']