# Create your models here.
from django.db import models


from django.conf import settings
from django.utils import timezone
import datetime
import uuid

from django.http import Http404, HttpResponseRedirect


from django.shortcuts import reverse

from mechanism.users import User


class NotificationType(models.TextChoices):
    NEW_AUCTION="0"
    OUTBID="1"
    AUCTION_AWARD="2"
    NEW_LIKE="3"
    NEW_BID="4"

    WINNER_LIED="5"
    REOPENING_FOR_ANY_REASON="6"
    AUCTION_EXPIRED="7"

class NotificationManager(models.Manager):
    def create_for_new_auction(self,receiver,auction):
        instance=self.create(
            receiver=receiver,
            link_id=auction.id,
            purpose=NotificationType.NEW_AUCTION,
        )

        return instance
    def create_for_new_bid(self,receiver,bidder):
        return self.create(
            receiver=receiver,
            link_id=bidder.id,
            purpose=NotificationType.NEW_BID,
        )
    def create_for_new_like(self,owner,liker):
        if owner == liker:  # avoid sailesh liked sailesh post.
            return

        return self.create(
            receiver=owner,
            link_id=liker.id,
            purpose=NotificationType.NEW_LIKE
        )
    
    def create_for_bid_winner(self,winner,link_id):
        
        return self.create(
            receiver=winner,
            link_id=link_id,
            purpose=NotificationType.AUCTION_AWARD
        )
    
    def create_for_notice_page(self,owner,liker):
        if owner == liker:  # avoid sailesh liked sailesh post.
            return

        return self.create (
            receiver=owner,
            link_id=liker.id,
            purpose=NotificationType.NEW_LIKE
        )




class Notification(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    objects=NotificationManager()

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
        return HttpResponseRedirect(reverse('notification_detail', args=[str(self.id)]))

    #todo 
    #notification
    def for_like(self):
        return False
    def for_outbid(self):
        return False
    def for_auction_award(self):
        return False
    
    def for_new_auction(self):
        return True