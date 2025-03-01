from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from users.models import Usuario
from .models import Tarea
import json

class TareaTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = Usuario.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword1'
        )
        
        self.user2 = Usuario.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
        )
        
        # Create test tareas
        self.tarea1 = Tarea.objects.create(
            title='Test Tarea 1',
            description='Test Description 1',
            completed=False,
            owner=self.user1
        )
        
        self.tarea2 = Tarea.objects.create(
            title='Test Tarea 2',
            description='Test Description 2',
            completed=True,
            owner=self.user1
        )
        
        self.tarea3 = Tarea.objects.create(
            title='Test Tarea 3',
            description='Test Description 3',
            completed=False,
            owner=self.user2
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_list_tareas(self):
        """Test that a user can only see their own tareas"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Get list of tareas
        response = self.client.get(reverse('tarea-list'))
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that only user1's tareas are returned
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Tarea 1')
        self.assertEqual(response.data[1]['title'], 'Test Tarea 2')
    
    def test_create_tarea(self):
        """Test creating a new tarea"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Create new tarea
        data = {
            'title': 'New Test Tarea',
            'description': 'New Test Description',
            'completed': False
        }
        
        response = self.client.post(
            reverse('tarea-create'),
            data,
            format='json'
        )
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that tarea was created with correct owner
        self.assertEqual(Tarea.objects.count(), 4)
        new_tarea = Tarea.objects.get(title='New Test Tarea')
        self.assertEqual(new_tarea.owner, self.user1)
    
    def test_create_tarea_with_invalid_title(self):
        """Test creating a tarea with a title that's too short"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Create new tarea with invalid title
        data = {
            'title': 'AB',  # Less than 3 characters
            'description': 'Test Description',
            'completed': False
        }
        
        response = self.client.post(
            reverse('tarea-create'),
            data,
            format='json'
        )
        
        # Check that creation was rejected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that no new tarea was created
        self.assertEqual(Tarea.objects.count(), 3)
    
    def test_update_tarea(self):
        """Test updating a tarea"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Update user1's tarea with PATCH (partial update)
        data = {
            'title': 'Updated Test Tarea',
            'description': 'Updated Test Description',
            'completed': True
        }
        
        response = self.client.patch(
            reverse('tarea-update', kwargs={'pk': self.tarea1.id}),
            data,
            format='json'
        )
        
        # Check that update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that tarea was updated
        self.tarea1.refresh_from_db()
        self.assertEqual(self.tarea1.title, 'Updated Test Tarea')
        self.assertEqual(self.tarea1.description, 'Updated Test Description')
        self.assertTrue(self.tarea1.completed)
    
    def test_update_tarea_single_field(self):
        """Test updating only one field of a tarea"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Update only the completed field
        data = {
            'completed': True
        }
        
        response = self.client.patch(
            reverse('tarea-update', kwargs={'pk': self.tarea1.id}),
            data,
            format='json'
        )
        
        # Check that update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that only the completed field was updated
        self.tarea1.refresh_from_db()
        self.assertEqual(self.tarea1.title, 'Test Tarea 1')  # Unchanged
        self.assertEqual(self.tarea1.description, 'Test Description 1')  # Unchanged
        self.assertTrue(self.tarea1.completed)  # Changed
    
    def test_update_tarea_invalid_field(self):
        """Test updating a tarea with an invalid field"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Try to update with an invalid field
        data = {
            'invalid_field': 'Some value'
        }
        
        response = self.client.patch(
            reverse('tarea-update', kwargs={'pk': self.tarea1.id}),
            data,
            format='json'
        )
        
        # Check that update was rejected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that tarea was not updated
        self.tarea1.refresh_from_db()
        self.assertEqual(self.tarea1.title, 'Test Tarea 1')
        self.assertEqual(self.tarea1.description, 'Test Description 1')
        self.assertFalse(self.tarea1.completed)
    
    def test_update_tarea_permission(self):
        """Test that a user can only update their own tareas"""
        # Login as user2
        self.client.force_authenticate(user=self.user2)
        
        # Try to update user1's tarea
        data = {
            'title': 'Updated Test Tarea',
            'description': 'Updated Test Description',
            'completed': True
        }
        
        response = self.client.patch(
            reverse('tarea-update', kwargs={'pk': self.tarea1.id}),
            data,
            format='json'
        )
        
        # Check that update was denied (404 because the queryset filters by owner)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Check that tarea was not updated
        self.tarea1.refresh_from_db()
        self.assertEqual(self.tarea1.title, 'Test Tarea 1')
    
    def test_delete_tarea(self):
        """Test deleting a tarea"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Delete user1's tarea
        response = self.client.delete(
            reverse('tarea-delete', kwargs={'pk': self.tarea1.id})
        )
        
        # Check that delete was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that tarea was deleted
        self.assertEqual(Tarea.objects.count(), 2)
        with self.assertRaises(Tarea.DoesNotExist):
            Tarea.objects.get(id=self.tarea1.id)
    
    def test_delete_tarea_permission(self):
        """Test that a user can only delete their own tareas"""
        # Login as user2
        self.client.force_authenticate(user=self.user2)
        
        # Try to delete user1's tarea
        response = self.client.delete(
            reverse('tarea-delete', kwargs={'pk': self.tarea1.id})
        )
        
        # Check that delete was denied (404 because the queryset filters by owner)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Check that tarea was not deleted
        self.assertEqual(Tarea.objects.count(), 3)
        self.tarea1.refresh_from_db()  # This would raise DoesNotExist if the tarea was deleted
    
    def test_filter_completed_tareas(self):
        """Test filtering tareas by completed status"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Get completed tareas
        response = self.client.get(reverse('tarea-filter-completed'))
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that only completed tareas are returned
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Tarea 2')
        self.assertTrue(response.data[0]['completed'])
    
    def test_detail_tarea(self):
        """Test retrieving a specific tarea"""
        # Login as user1
        self.client.force_authenticate(user=self.user1)
        
        # Get tarea details
        response = self.client.get(
            reverse('tarea-detail', kwargs={'pk': self.tarea1.id})
        )
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that correct tarea is returned
        self.assertEqual(response.data['title'], 'Test Tarea 1')
        self.assertEqual(response.data['description'], 'Test Description 1')
        self.assertFalse(response.data['completed'])
    
    def test_detail_tarea_permission(self):
        """Test that a user can only view their own tareas"""
        # Login as user2
        self.client.force_authenticate(user=self.user2)
        
        # Try to get user1's tarea
        response = self.client.get(
            reverse('tarea-detail', kwargs={'pk': self.tarea1.id})
        )
        
        # Check that access was denied (404 because the queryset filters by owner)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
