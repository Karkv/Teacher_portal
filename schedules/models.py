from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subject(models.Model):
    name = models.CharField(max_length=100)
    total_hours = models.FloatField()
    start_date = models.DateField(default=now, null=True, blank=True)  # Pass the callable 'now' without parentheses

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name="teachers")

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_teacher(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'teacher'):
        Teacher.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher(sender, instance, **kwargs):
    if hasattr(instance, 'teacher'):
        instance.teacher.save()

class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.teacher.user.username} - {self.subject.name} - {self.start_time}"

class Holiday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name
