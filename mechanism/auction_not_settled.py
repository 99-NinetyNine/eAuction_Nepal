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
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="not_settled")
    winner_index=models.IntegerField(default=0,blank=True,null=True)


    def __str__(self):
        return f"auction {str(self.auction.id)[0:4]}, just won by={self.winner.username}"

    def seven_days_elapsed(self):
        return True
    
    def get_current_winner(self):
        bids=self.auction.bids.all().order_by("-bid_amount")
        try:
            return bids[self.winner_index]
        except:
            return None
        
    def get_next_winner(self,):
        bids=self.auction.bids.all().order_by("-bid_amount")
        try:
            next_one=bids[self.next_winner_index]
            self.next_winner_index   +=  1
            self.save()
        except:
            next_one=None

        return next_one
