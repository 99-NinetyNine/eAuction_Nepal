# Create your models here.
from django.db import models


from django.conf import settings
from django.utils import timezone
import datetime
import uuid

from PIL import Image


from django.shortcuts import reverse

from django.contrib.auth import get_user_model
User=get_user_model()


class NotificationType(models.TextChoices):
    NEW_AUCTION="0"
    OUTBID="1"
    AUCTION_AWARD="2"
    LIKE="3"

class Notification(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    receiver = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE, default=None
    )

    link_id=models.CharField(max_length=100,blank=True,null=True)

    created=models.DateTimeField(default=timezone.now)

    purpose=models.CharField(max_length=1,choices=NotificationType.choices,default=NotificationType.NEW_AUCTION)

    is_checked=models.BooleanField(default=False, blank=True)
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        msg=""
        if(self.for_like()):
            msg="like"
        elif(self.for_new_auction()):
            msg="auction"
        elif(self.for_outbid()):
            msg="bid"
        elif(self.for_auction_award()):
            pass
        msg= msg+" "+"notification %s" %str(self.id)[0:4]
        return msg
    def get_absolute_url(self):
        return reverse('notification_detail', args=[str(self.id)])

    def for_like(self):
        return False
    def for_outbid(self):
        return False
    def for_auction_award(self):
        return False
    
    def for_new_auction(self):
        return True