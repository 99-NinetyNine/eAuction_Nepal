from django.test import TestCase,SimpleTestCase


# Create your tests here.
class SimpleTests(SimpleTestCase):
    def home_page(self):
        response=self.get('/')
        self.assertEqual(response.status_code,200)
        
