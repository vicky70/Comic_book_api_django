from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

from .models import Comic

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

