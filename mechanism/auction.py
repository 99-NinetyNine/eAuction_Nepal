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


import random
from django.contrib.auth import get_user_model
User=get_user_model()
# class Place(models.Model):
#     city = models.CharField(max_length=100)
#     location = PlainLocationField(based_fields=['city'], zoom=7)
from mechanism.notification import Notification

class AuctionManager(models.Manager):
    def get_queryset_for(self,user):
        return self.get_queryset()
    
    def for_index_page(self):
        qs=self.get_queryset()
        rd=random.randint(0,len(qs))
        new=qs[0:rd]
        old=qs[rd:]

        return [n.prepare_for_index_page() for n in new],[o.prepare_for_index_page() for o in old]
        
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

    #decremented after each admin login when case of close auction.
    semaphore=models.IntegerField(default=3,null=True,blank=True)

    class Meta:
        ordering = ["-pub_date"]

    def disclosed_by_admins(self):
        if(self.is_type_open()):
            return True
            
        return self.semaphore==0

    #otp for disclosing bids
    def get_otp_for_admins(self):
        print("otp are",1102,1021,1212)
        return 112,121,1212


    def check_otp_for_admins(self):
        return True

    def down_semaphore(self):
        #sysnchornization or memorization haha..??
        if(self.semaphore>0):
            self.semaphore  -=1
        else:
            print("errie")


    def get_bid_winner(self):
        biddings=self.bids.all()
        highest=biddings.first()
        for bidding in biddings:
            if bidding.bid_amount > highest.bid_amount:
                highest=bidding
        
        return highest.bidder

    def prepare_for_index_page(self,request=None):
        
        t=self.__dict__
        t["db"]=self
        t["fav"]=self.favourite.filter(id=request.user.id if request else 0).exists()    
        #print(t)
        return t

    def is_type_open(self):
        return self.open_close #open=1,close=0
    def is_he_bidder(self,some_user):
        return self.bids.filter(bidder=some_user).exists()
    def get_amount_he_bid(self,some_user):
        return self.bids.filter(bidder=some_user).first().bid_amount
        
    def bidding_not_started(self):
        return False
    def in_bidding_season(self):
        return True
    def bidding_season_closed(self):
        return False
    
    

    def prepare_for_detail_page(auction):
        return auction

    
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

