from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse("user-login")
        self.user_data = {
            "userName":"Alice",
            "userEmail":"alice@email.com",
            "userPhone":"012345",
            "password":"012345"
        }
        return super().setUp()