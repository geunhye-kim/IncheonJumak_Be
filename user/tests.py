from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User,Verify

class sendEmailTest(APITestCase):
    def setUp(self):
        self.url = reverse('send_email')
        
    def test_send_email(self):
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,200)
        
    def test_send_email_blank(self):
        email ={
            'email':''
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_send_email_not_email(self):
        email ={
            'email':'test'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_send_email_already_send_email(self):
        verify = Verify.objects.create(email='test@test.com',code='123456')
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        re_verify = Verify.objects.get(email=email['email'])
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(verify,re_verify.code)
    
    def test_send_email_already_register_email(self):
        User.objects.create(email='test@test.com',password='1234', nickname='test')
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)
        
class emailVerifyTest(APITestCase):
    def setUp(self):
        self.url = reverse('verify_email')
        self.verify = Verify.objects.create(email='test@test.com',code='123456')
        
    def test_email_verify(self):
        verify ={
            'email':'test@test.com',
            'code':'123456'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,200)
        
    def test_email_verify_not_match_code(self):
        verify ={
            'email':'test@test.com',
            'code':'654321'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_email_verify_not_match_email(self):
        verify ={
            'email':'test2@test.com',
            'code':'123456'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_email_verify_not_match_both(self):
        verify ={
            'email':'test2@test.com',
            'code':'654321'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
class signUpTest(APITestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.verify_t = Verify.objects.create(email='test@test.com',code='123456',verification=True)
        self.verify_f = Verify.objects.create(email='test2@test.com',code='123456')
        self.user = User.objects.create(email='test3@test.com',password='12345678@', nickname='test2')
        
    def test_sign_up(self):
        user ={
            'email':'test@test.com',
            'password':'test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,201)
        
    def test_sign_up_not_match_code(self):
        user ={
            'email':'test2@test.com',
            'password':'Test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_email(self):
        user ={
            'email':'test',
            'password':'Test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_include_lecture_in_password(self):
        user ={
            'email':'test',
            'password':'Test1234',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_over_min_length_password(self):
        user ={
            'email':'test',
            'password':'Test12@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_not_use_number_password(self):
        user ={
            'email':'test',
            'password':'testtest@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_use_alphabat_password(self):
        user ={
            'email':'test',
            'password':'13245678@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_overlapping_email(self):
        user ={
            'email':'test3@test.com',
            'password':'test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_overlapping_nickname(self):
        user ={
            'email':'test3@test.com',
            'password':'test1234@',
            'nickname':'test2',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)