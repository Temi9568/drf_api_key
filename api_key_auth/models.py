from typing import Iterable
from django.db import models
from django.utils import timezone
import secrets
from .managers import APIKeyManager


class APIKey(models.Model):
    """
    Model representing an API key.
    """
    key = models.CharField(max_length=100, unique=True, default=secrets.token_urlsafe)
    name = models.CharField(max_length=55)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = APIKeyManager()

    class Meta:
        verbose_name_plural = "API Keys"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure modified_at is updated.
        """
        super().save(*args, **kwargs)


class Request(models.Model):
    """
    Model representing a request made using an API key.
    """
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Requests"
        ordering = ['-created_at']

    def __str__(self):
        return f"Request by {self.api_key} on {self.created_at}"
