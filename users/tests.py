from django.test import TestCase,SimpleTestCase
from .models import (
    BidUser,
    Rating,
)
from django.contrib.auth import get_user_model

class SignUpTest(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'

    def test_signup_page_status_code(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_signup.html')
    
    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email


class RatingTest(TestCase):
    def setUp(self):
        self.resp=self.client.get(reverse('rate_user'))
    
    def test_basics(self):
        self.assertEqual(self.resp.status_code,200)
        self.assertTemplateUsed(response, 'users/rating_form.html')
