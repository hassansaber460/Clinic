from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.TimeField(auto_now=True, null=True)
    activate_assistant = models.BooleanField(default=False)
    activate_doctor = models.BooleanField(default=False)
    end_work = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.queue_id}|activate_doctor:{self.activate_doctor}"


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    room_receiving = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                       related_name='room_receiving')
    room_send = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='room_send')
    message = models.CharField(max_length=450)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.message} from {self.room_send.username} to {self.room_receiving.username}'
