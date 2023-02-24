# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import validators


from django.conf import settings
from django.utils import timezone

import datetime
import uuid

from django.shortcuts import reverse
from PIL import Image



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

    def get_absolute_url(self):
        return reverse('bid_detail', args=[str(self.id)])
    def __str__(self):
        return self.bidder.username+" bid %s" %str(self.id)[0:4]
    

    def bid_created_alert(instance):
        owner=instance.auction.user
        bidder=instance.bidder
        auction=instance.auction

        from mechanism.notification import Notification
        Notification.objects.create_for_new_bid(
            receiver=owner,
            bidder=bidder,
        )
