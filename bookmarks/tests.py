from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from .models import Bookmark
from django.db import IntegrityError

class BookmarkTestCase(TestCase):
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
            longitude=109.00,  # Koordinat yang tidak memenuhi kondisi apapun
            latitude=-7.70
        )

        # Client untuk pengguna terautentikasi
        self.client1 = Client()
        self.client1.login(username='user1', password='password1')

        # Client untuk pengguna kedua
        self.client2 = Client()
        self.client2.login(username='user2', password='password2')

        # Client untuk pengguna tidak terautentikasi
        self.client_unauthenticated = Client()

    def test_add_bookmark_authenticated_user(self):
        """Test menambahkan bookmark oleh pengguna terautentikasi."""
        url = reverse('bookmarks:toggle_bookmark')
        response = self.client1.post(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)  # UUID sebagai string

        # Pastikan bookmark dibuat
        bookmark_exists = Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant1).exists()
        self.assertTrue(bookmark_exists)

    def test_remove_bookmark_authenticated_user(self):
        """Test menghapus bookmark oleh pengguna terautentikasi."""
        # Tambahkan bookmark terlebih dahulu
        bookmark = Bookmark.objects.create(user=self.user1, restaurant=self.restaurant1)
        url = reverse('bookmarks:toggle_bookmark')
        response = self.client1.post(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertFalse(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Bookmark removed successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsNone(json_response['bookmark_id'])

        # Pastikan bookmark dihapus
        bookmark_exists = Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant1).exists()
        self.assertFalse(bookmark_exists)

    def test_toggle_bookmark_multiple_times(self):
        """Test toggling bookmark berulang kali."""
        url = reverse('bookmarks:toggle_bookmark')

        # Toggle pertama: tambah bookmark
        response = self.client1.post(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)
        self.assertTrue(Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant1).exists())

        # Toggle kedua: hapus bookmark
        response = self.client1.post(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertFalse(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Bookmark removed successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsNone(json_response['bookmark_id'])
        self.assertFalse(Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant1).exists())

        # Toggle ketiga: tambah kembali
        response = self.client1.post(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)
        self.assertTrue(Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant1).exists())

    def test_add_bookmark_different_users(self):
        """Test bahwa pengguna kedua dapat menambahkan bookmark tanpa mempengaruhi pengguna pertama."""
        url = reverse('bookmarks:toggle_bookmark')

        # Pengguna pertama menambahkan bookmark
        response = self.client1.post(url, {'restaurant_id': self.restaurant2.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)
        self.assertTrue(Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant2).exists())

        # Pengguna kedua menambahkan bookmark yang sama
        response = self.client2.post(url, {'restaurant_id': self.restaurant2.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)
        self.assertTrue(Bookmark.objects.filter(user=self.user2, restaurant=self.restaurant2).exists())

        # Pastikan kedua bookmark ada
        bookmarks_user1 = Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant2).count()
        bookmarks_user2 = Bookmark.objects.filter(user=self.user2, restaurant=self.restaurant2).count()
        self.assertEqual(bookmarks_user1, 1)
        self.assertEqual(bookmarks_user2, 1)

    def test_toggle_bookmark_with_invalid_restaurant_id(self):
        """Test toggling bookmark dengan ID restoran yang tidak valid."""
        url = reverse('bookmarks:toggle_bookmark')
        invalid_id = 'invalid_id'  # Mengirim restaurant_id yang tidak valid
        response = self.client1.post(url, {'restaurant_id': invalid_id})
        self.assertEqual(response.status_code, 400)  # Sesuai dengan view yang diperbarui
        json_response = response.json()
        self.assertIn('error', json_response)
        self.assertEqual(json_response['error'], 'Invalid restaurant ID format')

    def test_toggle_bookmark_unauthenticated_user(self):
        """Test bahwa pengguna tidak terautentikasi tidak bisa toggle bookmark."""
        url = reverse('bookmarks:toggle_bookmark')
        response = self.client_unauthenticated.post(url, {'restaurant_id': self.restaurant1.id})
        # Redirect ke halaman login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))  # Sesuaikan URL login jika berbeda

    def test_prevent_duplicate_bookmarks(self):
        """Test bahwa pengguna tidak bisa membuat bookmark ganda."""
        url = reverse('bookmarks:toggle_bookmark')

        # Tambahkan bookmark pertama kali
        response = self.client1.post(url, {'restaurant_id': self.restaurant3.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)
        self.assertEqual(Bookmark.objects.filter(user=self.user1, restaurant=self.restaurant3).count(), 1)

        # Coba tambahkan bookmark lagi secara manual
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(user=self.user1, restaurant=self.restaurant3)  # Harus gagal karena unique_together

    def test_remove_nonexistent_bookmark(self):
        """Test menghapus bookmark yang belum ada."""
        url = reverse('bookmarks:toggle_bookmark')

        # Coba hapus bookmark yang belum ada (toggle akan menambah bookmark)
        response = self.client1.post(url, {'restaurant_id': self.restaurant2.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)

        # Hapus bookmark pertama kali
        response = self.client1.post(url, {'restaurant_id': self.restaurant2.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertFalse(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Bookmark removed successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsNone(json_response['bookmark_id'])

        # Coba hapus lagi (toggle akan menambah kembali bookmark)
        response = self.client1.post(url, {'restaurant_id': self.restaurant2.id})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('is_bookmarked', json_response)
        self.assertTrue(json_response['is_bookmarked'])
        self.assertIn('success', json_response)
        self.assertTrue(json_response['success'])
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Restaurant bookmarked successfully')
        self.assertIn('bookmark_id', json_response)
        self.assertIsInstance(json_response['bookmark_id'], str)

    def test_toggle_bookmark_with_invalid_method(self):
        """Test bahwa metode selain POST tidak diizinkan."""
        url = reverse('bookmarks:toggle_bookmark')
        response = self.client1.get(url, {'restaurant_id': self.restaurant1.id})
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_get_location_default(self):
        """Test bahwa get_location mengembalikan 'Yogyakarta Barat' jika koordinat tidak sesuai kondisi."""
        restaurant = self.restaurant4  # longitude=109.00, latitude=-7.70
        self.assertEqual(restaurant.get_location(), "Yogyakarta Barat")
        
    def test_bookmark_str(self):
        """Test __str__ method of Bookmark model."""
        bookmark = Bookmark.objects.create(user=self.user1, restaurant=self.restaurant1)
        expected_str = f"{self.user1.username} bookmarks {self.restaurant1.name}"
        self.assertEqual(str(bookmark), expected_str)

