from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    pass


@receiver(post_save, sender=User)
def create_iot_token(sender, instance=None, created=False, **kwargs):
    pass
