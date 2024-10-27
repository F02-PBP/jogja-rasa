from django.forms import ModelForm
from .models import Review

class ReviewRestaurantForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review"]