from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_user_token(sender, instance=None, created=False, *args, **kwargs):
   
   if created:
       token = Token.objects.create(user=instance)
       token.save()