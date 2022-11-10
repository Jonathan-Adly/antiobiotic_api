from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name.
    stripe_cust = models.CharField(max_length=250, blank=True)
    stripe_sub = models.CharField(max_length=250, blank=True)
    subscribe_to_emails = models.BooleanField(default=True)


# create token on registeration
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
