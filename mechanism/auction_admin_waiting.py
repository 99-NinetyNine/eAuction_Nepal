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


class AdminWaitingAuction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="waiting_admin")
    #decremented after each admin login when case of close auction.
    semaphore=models.IntegerField(default=3,null=True,blank=True)

    def __str__(self):
        return f"auction waiting to admin {str(self.auction.id)[0:4]}"

    def down_semaphore(self):
        #sysnchornization or memorization haha..??
        if(self.semaphore>0):
            self.semaphore  -=1
            self.save()
            return True
        
        return False
