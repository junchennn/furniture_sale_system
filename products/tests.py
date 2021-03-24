from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Product


# Create your tests here.
User = get_user_model()

class ProductTestCase(TestCase):

    def setUp(self): # camel case - python's builtin unit test
        user_a = User(username='jtest', email='jtest@gmail.com')
        # User.objects.create_user()
        user_a_pw = 'dingdong123'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        user_b = User.objects.create_user('user_2', 'user_2@gmail.com', 'dingdong123')
        self.user_b = user_b

    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_invalid_request(self):
        self.client.login(username=self.user_b.username, password='dingdong123')
        response = self.client.post("/products/create/",{
            "title": "this is an valid test"
        })
        # self.assertTrue(response.status_code!=200) #201
        self.assertNotEqual(response.status_code, 200) 

    def test_valid_request(self):
        self.client.login(username=self.user_a.username, password='dingdong123')
        response = self.client.post("/products/create/",{
            "title": "this is an valid test"
        })
        # self.assertTrue(response.status_code==200) #201
        self.assertEqual(response.status_code, 200) 
