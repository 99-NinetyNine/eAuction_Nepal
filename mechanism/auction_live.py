from django.db import models

import uuid

from django.utils import timezone
import datetime

from django.conf import settings

from django.shortcuts import reverse


import random


from mechanism.notification import Notification
from mechanism.auction import Auction

class LiveAuction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="live")
    

    def __str__(self):
        return f"live auction {str(self.auction.id)[0:4]}"
