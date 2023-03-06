from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import validators
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

import uuid

from django.utils import timezone
import datetime

from django.conf import settings

from django.shortcuts import reverse


from django.contrib.auth import get_user_model
User=get_user_model()
# class Place(models.Model):
#     city = models.CharField(max_length=100)
#     location = PlainLocationField(based_fields=['city'], zoom=7)
from mechanism.notification import Notification

class AuctionManager(models.Manager):
    def get_queryset_for(self,user):
        return self.get_queryset()
        
    def get_serialized_query_set(self,query_set,request,single_item=False):
        """
        returns a list of ["auction instance","is_liked","is_disliked","is_favourite"]
        """
        res=[]
        
        if(single_item):
            res.append(query_set)
            res.append(query_set.upvotes.filter(id=request.user.id).exists())
            res.append(query_set.downvotes.filter(id=request.user.id).exists())
            res.append(query_set.favourite.filter(id=request.user.id).exists())
            
            #note that i need list of lists haha..for unpacking
            res2=[]
            res2.append(res)
            return res2


        for q in query_set:
            t=[]
            t.append(q)
            t.append(q.upvotes.filter(id=request.user.id).exists())
            t.append(q.downvotes.filter(id=request.user.id).exists())
            t.append(q.favourite.filter(id=request.user.id).exists())
            res.append(t)
        
        return res

    

    def get_highest_bidder(self,auction):
            biddings=auction.bids.all()
            highest=biddings.first()
            for bidding in biddings:
                if bidding.bid_amount > highest.bid_amount:
                    highest=bidding
            
            return highest

class Auction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    query=AuctionManager()
    objects=models.Manager()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction")
    title=models.CharField(max_length=30,blank=False,null=True)
    description = models.CharField(max_length=200, blank=False,null=True)
    youtube=models.CharField(max_length=100,blank=True,null=True)
    thumbnail=models.ImageField(upload_to="AuctionImages/",null=True,)
    #
    open_close=models.BooleanField(default=False)
    #false=open
    #
    
    saved_confirmed=models.BooleanField(default=False)
    #false=saved
    
    #product
    product_shipped=models.BooleanField(default=False)

    #location = models.OneToOneField(Place, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name="likes", blank=True)
    downvotes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    favourite = models.ManyToManyField(User, related_name="favourites", blank=True)
    hide_post = models.BooleanField(default=False, blank=True)
    

    pdf=models.FileField(upload_to="Auction_pdf/")
    price_min_value= models.IntegerField(default=1)
    price_max_value=models.IntegerField(default=100)

    pub_date = models.DateTimeField(default=timezone.now)
    expiry_date=models.DateTimeField(default=timezone.now)  #put it 7 days later
        

    class Meta:
        ordering = ["-pub_date"]

    @staticmethod
    def prepare_for_detail_page(auction):
        return auction

    #otp for disclosing bids
    def get_otp_for_admins(self):
        return 112,121,1212
    def get_otp_for_adminA(self):
        return 1
    def get_otp_for_adminB(self):
        return 1
    def get_otp_for_adminC(self):
        return 1
    #notifications
    def new_like_notification(self,liker):
        Notification.objects.create_for_new_like(self.user, liker)
    def send_notice_to_page(self):
        pass
    
    def send_notice_to_news(self):
        pass


    def bidder_paid_initial(self,bidder):
        return False
    
    def bidder_paid_remaining(self,bidder):
    
        return False

    def adminA_logged_in(self):
        return False
    
    def adminB_logged_in(self):
        return False
    
    def adminC_logged_in(self):
        return False
    def increase_cutoff(self):
        return 1
    def has_product_shipped(self):
        return False
    
    def winner_didnot_paid_money_handler(self):
        pass
    
    def schedule_expiry_logic(self):
        pass
    
    def schedule_bid_won_logic(self):
        pass

    
    def auction_created_alert(instance):
        """
        user x created an auction.
        Brodcast to [user_lists] users
        """
        x=instance.user
        user_lists=x.get_my_subscribers()
        
        
        for u in user_lists:
            Notification.objects.create_for_new_auction(
                receiver=u,
                auction=instance,
            )
        print("user x created an auction Brodcast to [user_lists] users")

    def get_bids_by_order(self):
        from django.db.models import Avg
        qs=self.bids.annotate(ratings=Avg('bidder__to__rating')).order_by('bid_amount','-ratings')
        return qs
    def get_youtube(self):
        return f"https://www.youtube.com/embed/{self.youtube}?autoplay=1&mute=1&loop=1&controls=0"
        
    def get_highest_bidder(self):
        return Auction.query.get_highest_bidder(self)

    def is_new_bid_okay(self,bidder,bid_amount):
        if self.user == bidder:
            return False
        highest_bidding=self.get_highest_bidder()
        
        if(highest_bidding.user==bidder):
            return False
        
        if(highest_bidding.bid_amount<=bid_amount):
            return False
        
        return True
    def __str__(self):
        return self.user.username +" auction %s" %str(self.id)[0:4]

    def total_upvotes(self):
        return self.upvotes.count()

    def get_absolute_url(self):
        return reverse("auction_detail", args=[str(self.id)])

    def has_expired(self):
        if(self.expiry_date<= timezone.now()):
            return False
        return True

