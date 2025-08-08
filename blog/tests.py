from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

class BlogPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        

    def test_list_blog_posts(self):
        response = self.client.get('/api/blog/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_blog_post(self):
        response = self.client.get('/api/blog/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_blog_post(self):
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            
        }
        response = self.client.post('/api/blog/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_blog_post(self):
        data = {
            'title': 'Updated Post',
            'content': 'This is an updated post.',
            
        }
        response = self.client.put('/api/blog/posts/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_blog_post(self):
        response = self.client.delete('/api/blog/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


