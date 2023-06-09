from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, List, Item, Comment
from .serializers import ProjectSerializer, ListSerializer, ItemSerializer, CommentSerializer

class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(title='Test Project',owner=1)
        self.list = List.objects.create(project=self.project, title='Test List')
        self.item = Item.objects.create(list=self.list, title='Test Item')
        self.comment = Comment.objects.create(item=self.item, body='Test Comment')

    def test_add_project(self):
        url = reverse('add_project')
        data = {
            'project': {
                'title': 'New Project',
                'description': 'Project description'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_projects_by_user(self):
        url = reverse('projects_by_user', args=[self.project.owner])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.project.title)

    def test_project_by_id(self):
        url = reverse('project_by_id', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)

    def test_add_list(self):
        url = reverse('add_list')
        data = {
            'project': self.project.pk,
            'title': 'New List'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(List.objects.count(), 2)

    def test_add_item(self):
        url = reverse('add_item')
        data = {
            'list': self.list.pk,
            'title': 'New Item'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_comments_by_item(self):
        url = reverse('comments_by_item', args=[self.item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['body'], self.comment.body)


