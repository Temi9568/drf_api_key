from django.db import models
import secrets


class APIKeyManager(models.Manager):
    def replace_key(self, api_key_obj):
        """
        Replaces the key of the given APIKey instance.

        Args:
            api_key_instance (APIKey): An instance of the APIKey model.

        Returns:
            APIKey: The APIKey instance with the replaced key.
        """
        api_key_obj.key = secrets.token_urlsafe()
        api_key_obj.save(update_fields=['key'])
        return api_key_obj