from django.db import models

from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings

import datetime
import uuid
import random

from mechanism.users import User

from mechanism.notification import Notification
from mechanism.auction import Auction


class RescheduleAuction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="re_schedule")
    

    def __str__(self):
        return f"auction to reschedule {str(self.auction.id)[0:4]}"
