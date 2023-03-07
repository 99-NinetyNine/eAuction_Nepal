#Although  a signle bollean field does the job, but filter(is_settled=True/False)..may be expensive??

from django.db import models

from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings


import datetime
import uuid
import random

from django.contrib.auth import get_user_model
User=get_user_model()

from mechanism.notification import Notification
from mechanism.auction import Auction


class NotSettledAuction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="unsettled")
    winner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="just_won")



    def __str__(self):
        return f"auction {str(self.auction.id)[0:4]}, just won by={self.winner.username}"
