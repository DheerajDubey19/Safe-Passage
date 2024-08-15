from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import File
import os
from django.conf import settings

class FileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.ops_user = User.objects.create_user(email='ops@example.com', password='password', role='ops')
        self.client_user = User.objects.create_user(email='client@example.com', password='password', role='client', verified=True)
        self.file = File.objects.create(file='uploads/test.docx', uploaded_by=self.ops_user)

    def test_upload_file(self):
        self.client.force_authenticate(user=self.ops_user)
        url = reverse('file-upload_file')
        with open(os.path.join(settings.BASE_DIR, 'uploads/test.docx'), 'rb') as test_file:
            response = self.client.post(url, {'file': test_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_generate_download_link(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('file-generate_download_link', args=[self.file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('download_link', response.data)

    def test_download_file(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('file-download_file', args=[self.file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{os.path.basename(self.file.file.name)}"')
