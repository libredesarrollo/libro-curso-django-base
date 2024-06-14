from django.test import Client, TestCase
from django.contrib.auth.models import User
class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_superuser(username='testuser', password='hjh5D4Aj4<')

        return super().setUp()
    
    def test_auth_admin(self):
        self.client.login(username='testuser', password='hjh5D4Aj4<')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()