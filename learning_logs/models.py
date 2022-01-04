from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS_CHOICES = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
]


class Topic(models.Model):
    """A topic the user is learning about"""
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(
        Topic, related_name='entries', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    chapter_number = models.PositiveIntegerField(null=True, blank=True)
    # status = models
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="New")

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entrys"

    def __str__(self):
        return self.text[:50] + "..."
