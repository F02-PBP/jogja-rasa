import json
from django.test import TestCase, Client
from .models import Reservation
from django.urls import reverse
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from .models import Reservation
from datetime import date, time

class ReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            longitude=123.45,
            latitude=-123.45,
            description='Test restaurant description'
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            date=date.today(),
            time=time(12, 30),
            number_of_people=2
        )

    def test_cannot_access_reservasi_if_not_logged_in(self):
        response = self.client.get('/reservasi/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/reservasi/'))

    def test_reservasi_url_is_accessible_for_logged_in_user(self):
        # Login terlebih dahulu
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/reservasi/')
        self.assertEqual(response.status_code, 200)
    
    def test_reservasi_using_reservation_template(self):
        # Login terlebih dahulu
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/reservasi/')
        self.assertTemplateUsed(response, 'reservation.html')
    
    def test_nonexistent_page(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/reservasi/sigma')
        self.assertEqual(response.status_code, 404)

    def test_delete_reservation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('reservation:delete_reservation', args=[str(self.reservation.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_edit_reservation(self):
        self.client.login(username='testuser', password='12345')
        updated_data = {
            'date': str(date.today()),
            'time': '13:00',
            'number_of_people': 3
        }
        response = self.client.post(
            reverse('reservation:edit_reservation', args=[str(self.reservation.id)]),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_reservation = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(updated_reservation.time, time(13, 0))
        self.assertEqual(updated_reservation.number_of_people, 3)

    def test_show_json_by_id(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('reservation:show_json_by_id', args=[str(self.reservation.id)]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], str(self.reservation.id))

    def test_show_json(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('reservation:show_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], str(self.reservation.id))

    def test_access_without_login(self):
        response = self.client.get(reverse('reservation:show_reservation'))
        self.assertEqual(response.status_code, 302)  # Redirect to login