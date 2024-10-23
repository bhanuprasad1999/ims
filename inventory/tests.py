from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from inventory.models import InventoryModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
import json

class InventoryAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
        self.item_data = {
            'item_name': 'Test Item',
            'description': 'This is a test item',
            'quantity': 10,
            'unit':'units',
            'price': 100.0
        }
        self.item = InventoryModel.objects.create(**self.item_data)

    def test_create_item(self):
        response = self.client.post(reverse('create'), data=json.dumps(self.item_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['item_name'], self.item_data['item_name'])


    def test_manipulation_on_item_get(self):
        response = self.client.get(reverse('get-item') + f'?item_id={self.item.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['item_name'], self.item_data['item_name'])

    def test_manipulation_on_item_put(self):
        updated_data = {'item_name': 'Updated Item'}
        response = self.client.put(reverse('update-item')+ f'?item_id={self.item.id}',data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.item.refresh_from_db()
        self.assertEqual(self.item.item_name, updated_data['item_name'])

    def test_manipulation_on_item_delete(self):
        response = self.client.delete(reverse('delete-item')+ f'?item_id={self.item.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Successfully deleted')
        self.assertFalse(InventoryModel.objects.filter(id=self.item.id).exists())

    def test_manipulation_on_item_not_found(self):
        response = self.client.get(reverse('get-item'), {'item_id': 99999})  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['message'], 'Item not found')
