from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Comic, Reviews

# Create your tests here.

class TestAllComicEndPoint(TestCase):
    def generate_test_image(self):
        img_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return SimpleUploadedFile("test.jpg", img_io.read(), content_type="image/jpeg")
    
    def setUp(self):
        Comic.objects.create(
            name = 'batman comics',
            category = 'DC',
            description = 'this is a awsome comics from DC',
            original_price = 600,
            discounted_price = 500,
            rent_price = 7,
            comic_image = self.generate_test_image()
        )
        Comic.objects.create(
            name = 'ironman comics',
            category = 'Marvel',
            description = 'This is a ironman comic best of all time',
            original_price = 1200,
            discounted_price = 900,
            rent_price = 7,
            comic_image = self.generate_test_image()
        )


    def test_get_all_comics(self):
        url = reverse('AllComics')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

class TestUpdateReview(TestCase):
    def generate_test_image(self):
        img_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return SimpleUploadedFile("test.jpg", img_io.read(), content_type="image/jpeg")
    
    def setUp(self):
        self.client = APIClient()
        self.comic = Comic.objects.create(
            name = 'batman comic',
            category = 'DC',
            description = 'some description',
            original_price = 600,
            discounted_price = 500,
            rent_price = 7,
            comic_image = self.generate_test_image()
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.token = Token.objects.create(user=self.user)

        self.review = Reviews.objects.create(
            user = self.user,
            reviews_on_comic = self.comic,
            user_review = 'batman comic is the best',
            number_of_stars = 3
        )
    def test_review_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
        'user_review': 'Updated review text',
        'number_of_stars': 5
        }

        response = self.client.patch(f'/api/updateReview/{self.comic.id}/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['user_review'], 'Updated review text')
        self.assertEqual(response.data['data']['number_of_stars'], 5)

        # Refresh from DB to confirm update
        self.review.refresh_from_db()
        self.assertEqual(self.review.user_review, 'Updated review text')
        self.assertEqual(self.review.number_of_stars, 5)




