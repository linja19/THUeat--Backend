from .test_setup import TestSetUp
from api.models import User,Token
from django.urls import reverse

# Create your tests here.
class AccountTests(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.data["code"],400)

    def test_user_can_register(self):
        res = self.client.post(self.register_url,self.user_data)
        self.assertEqual(res.data["code"],200)

    def test_user_cannot_login_without_verification(self):
        self.client.post(self.register_url, self.user_data)
        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.data["code"],400)

    def test_user_can_login_after_verification(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(userName=self.user_data["userName"])
        user.is_active = True
        user.save()
        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.data["code"],200)

    def test_user_can_get_details_with_token(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(userName=self.user_data["userName"])
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user.pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.get(reverse("public-user-detail"))
        self.assertEqual(res.data["code"],200)

    def test_user_cannot_get_details_without_token(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(userName=self.user_data["userName"])
        user.is_active = True
        user.save()
        res = self.client.get(reverse("public-user-detail"))
        self.assertEqual(res.data["code"],400)