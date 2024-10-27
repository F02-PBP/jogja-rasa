from django.db import models
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField()

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name
    
    def get_location(self):
        if self.longitude >= 110.70:
            return "Solo"
        elif 110.38 <= self.longitude <= 110.41 or self.longitude >= 110.41:
            return "Yogyakarta Timur"
        elif 110.35 <= self.longitude <= 110.38:
            return "Yogyakarta Pusat"
        elif 110.32 <= self.longitude <= 110.35 or self.longitude <= 110.32:
            return "Yogyakarta Barat"
        elif -7.770 >= self.latitude >= -7.750:  
            return "Yogyakarta Utara"
        elif -7.820 <= self.latitude <= -7.810: 
            return "Yogyakarta Selatan"
        
        return "Yogyakarta" 