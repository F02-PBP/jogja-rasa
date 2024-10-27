from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from .models import Review
import datetime
import json
class ReviewTest(TestCase):
    def setUp(self):
        # Membuat pengguna

        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Membuat restoran
        self.restaurant1 = Restaurant.objects.create(
            name='Restoran A',
            description='Deskripsi Restoran A',
            longitude=110.40,
            latitude=-7.76
        )
        self.restaurant2 = Restaurant.objects.create(
            name='Restoran B',
            description='Deskripsi Restoran B',
            longitude=110.42,
            latitude=-7.81
        )
        self.restaurant3 = Restaurant.objects.create(
            name='Restoran C',
            description='Deskripsi Restoran C',
            longitude=110.30,
            latitude=-7.76
        )
        self.restaurant4 = Restaurant.objects.create(
            name='Restoran D',
            description='Deskripsi Restoran D',
            longitude=97.00,  # Koordinat yang tidak memenuhi kondisi apapun
            latitude=39.700
        )

        # Client untuk pengguna terautentikasi
        self.client1 = Client()
        self.client1.login(username='user1', password='password1')

        # Client untuk pengguna kedua
        self.client2 = Client()
        self.client2.login(username='user2', password='password2')

        # Client untuk pengguna tidak terautentikasi
        self.client_unauthenticated = Client()

        self.review = Review.objects.create(
            user=self.user1,
            restaurant=self.restaurant1,
            date=datetime.date.today(),
            rating=5,
            review="Great food!"
        )
    
    def test_add_review_authenticated_user(self):
        url = reverse('review:create_review')
        response = self.client1.post(url, {
            'review': 'good',
            'rating': 5,
            'pk_resto': self.restaurant1.id,
        })
        self.assertEqual(response.status_code, 201)

    def test_show_review(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client1.get(reverse('review:show_review'))
        self.assertEqual(response.status_code, 302)
    
    def test_show_review_more(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('review:show_review_more', args=[self.restaurant2.id]))
        self.assertEqual(response.status_code, 302)

    def test_show_restaurants_json(self):
        response = self.client.get(reverse('review:show_restaurants_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['fields']['name'], 'Restoran A')

    def test_show_reviews_json(self):
        response = self.client.get(reverse('review:show_reviews_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['review'], 'Great food!')
