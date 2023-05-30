from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.db.models import Max
from django.utils import timezone


class Project(models.Model):
    owner = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    members = ArrayField(models.PositiveIntegerField(),blank=True, null=True)
    image_url=models.CharField(blank=True, null=True)

    def __str__(self):
        return self.title
    def get_lists(self):
        return self.lists.all().order_by('order')


class List(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=255, blank=False, null=False)
    order = models.DecimalField(max_digits=30, decimal_places=15 , blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title



class Item(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    color = models.CharField(blank=True, null=False, max_length=6)  # Hex Code
    order = models.DecimalField(max_digits=30,decimal_places=15, blank=True, null=True)
    assigned_to = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.PositiveIntegerField(blank=True, null=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body
