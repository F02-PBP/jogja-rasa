from django.contrib.auth.models import User
from django.db import models
from restaurants.models import Restaurant

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarks {self.restaurant.name}"
