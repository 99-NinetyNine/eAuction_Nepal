# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import validators


from django.conf import settings
from django.utils import timezone

import datetime
import uuid

from django.shortcuts import reverse




from django.contrib.auth import get_user_model
User=get_user_model()

from mechanism.auction import Auction

class Bid(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    bidder=models.ForeignKey(User,on_delete=models.CASCADE,related_name="filled_bids")
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE,related_name="bids")
    
    bid_amount=models.FloatField(default=0)
    

    
    bail_trn_id=models.CharField(max_length=120,blank=False,null=True)
    remaining_trn_id=models.CharField(max_length=120,blank=False,null=True)

    #bidding can be saved for conriming later
    #todo
    saved_confirmed=models.BooleanField(default=False)


    ##################                  GETTERS             ##################
    ##################                  GETTERS             ##################
    ##################                  GETTERS             ##################
    
    def get_absolute_url(self):
        return reverse('bid_detail', args=[str(self.id)])
    def __str__(self):
        return self.bidder.username+" bid %s" %str(self.id)[0:4]
    
    
    ##################                  SETTERS             ##################
    ##################                  SETTERS             ##################
    ##################                  SETTERS             ##################
    
    def mark_remaining_paid(self,txn):
        self.remaining_trn_id=txn
        self.save()
        
    ##################                  CHECKERS             ##################
    ##################                  CHECKERS             ##################
    

    def has_bid(self):
        #just depositing the 10% amount and not actually quoted bid.
        return self.bid_amount >0

    def initial_paid(self):
        return self.bail_trn_id!=""

    def final_paid(self):
        return self.remaining_trn_id!=""
    
    ##################                  NOTIFICATION +++TODO             ##################
    ##################                  NOTIFICATION +++TODO             ##################
    
    def bid_created_alert(instance):
        owner=instance.auction.user
        bidder=instance.bidder
        auction=instance.auction

        from mechanism.notification import Notification
        Notification.objects.create_for_new_bid(
            receiver=owner,
            bidder=bidder,
        )
