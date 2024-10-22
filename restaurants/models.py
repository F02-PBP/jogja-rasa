from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField()

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name
