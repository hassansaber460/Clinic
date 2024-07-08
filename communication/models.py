from django.db import models
from django.utils import timezone


# Create your models here.
class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.TimeField(null=True)
    activate_assistant = models.BooleanField(default=False)
    activate_doctor = models.BooleanField(default=False)
    end_work = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.queue_id}|activate_doctor:{self.activate_doctor}"
