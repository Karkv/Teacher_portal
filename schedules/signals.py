# schedules/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher

@receiver(post_save, sender=User)
def create_teacher(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher(sender, instance, **kwargs):
    try:
        instance.teacher.save()
    except Teacher.DoesNotExist:
        # This handles cases where a user exists but no teacher was created initially
        Teacher.objects.create(user=instance)
