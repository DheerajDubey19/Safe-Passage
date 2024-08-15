from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User
import uuid

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.ops_user = User.objects.create_user(email='ops@example.com', password='password', role='ops')
        self.client_user = User.objects.create_user(email='client@example.com', password='password', role='client', verified=True)
        self.unverified_client_user = User.objects.create_user(email='unverified_client@example.com', password='password', role='client')

    def test_register_ops_user(self):
        url = reverse('user-register_ops')
        data = {'email': 'new_ops@example.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email='new_ops@example.com').exists(), True)

    def test_verify_email(self):
        verification_token = uuid.uuid4().hex
        self.unverified_client_user.verification_token = verification_token
        self.unverified_client_user.save()
        
        url = reverse('verify-email') + f'?verification_token={verification_token}'
        response = self.client.get(url)
        self.unverified_client_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.unverified_client_user.verified, True)
        self.assertEqual(self.unverified_client_user.verification_token, None)

    def test_login_ops_user(self):
        url = reverse('login_ops')
        data = {'email': self.ops_user.email, 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to upload_file

    def test_login_client_user(self):
        url = reverse('login_client')
        data = {'email': self.client_user.email, 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to list_files

    def test_signup_ops_user(self):
        url = reverse('signup_ops')
        data = {'email': 'new_ops_signup@example.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(email='new_ops_signup@example.com').exists(), True)

    def test_signup_client_user(self):
        url = reverse('signup_client')
        data = {'email': 'new_client_signup@example.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(email='new_client_signup@example.com').exists(), True)

    def test_logout_user(self):
        self.client.force_authenticate(user=self.ops_user)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to home

    def test_upload_file_view_unauthorized(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('upload_file')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Unauthorized", response.content.decode())

    def test_list_files_view(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('list_files')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
