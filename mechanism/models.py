from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
import uuid

class User(AbstractUser):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    profile_pic= models.ImageField(default="default.jpg", upload_to="ProfileImages/")
    phone_num=models.PositiveBigIntegerField(null=True,blank=True,unique=True)
    bio=models.CharField(max_length=100,blank=False,null=True)
    latitude=models.CharField(max_length=20,blank=False,null=True)
    longitude=models.CharField(max_length=20,blank=False,null=True)
    phone_verified=models.BooleanField(default=False)
    

    
    def has_verified_phone(self):
        return self.phone_verified

    def get_absolute_url(self):
        return reverse('profile_view', args=[str(self.id)])
    def get_update_url(self):
        return reverse('change_profile')
    def my_ratings(self):
        value=self.to.aggregate(models.Avg('rating'))
        return value['rating__avg']
        
        

class Rating(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='src')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to')
    
    #useful for ai..show those users who u rated max
    RATING_CHOICES= [
        ('0','No rating'),
        ('1','Poor'),
        ('2','Satisfactory'),
        ('3','Good'),
        ('4','Better'),
        ('5','Excellent'),
    ]
    rating=models.CharField(
        max_length=1,
        choices=RATING_CHOICES,
        default='3',
    )
    def __str__(self):
        return self.from_user.username +" to " + self.to_user.username
    
    def bids_removed_alert(sender, instance, **kwargs):
        if instance:
            """
            remove that notifin which says
            x posted bid on auction y
            
            instance.auction.user.bid_list.filter(user_by=instance.user,bid=instance.id or None,is_like=False).delete()
            """

            
        

    def bids_created_alert(sender, instance, **kwargs):
        if instance.user:
            
            x=instance.auction.user
            y=instance.user
            A=instance.auction

            if not x == y:
                """
                Not available option for modified operation so check once.
                """
                if not x.bids_alert.filter(
                    other_user=y, bid=instance.id or None, is_like=False
                ).exists():
                    Notification.objects.create(
                        receiver=x,
                        other_user=y,
                        auction=A,
                        bid=instance,
                        is_like=False,                    
                    )

    def get_users_auction(user_not_needed):
        """
        Bunch of users to whom notification is to be sent. Can obtained by using AI(skills and ratings and past experience)

        """
        return User.objects.exclude(id=user_not_needed.id)

    
def auction_created_alert(sender, instance,update_fields,**kwargs):
    """
    user x created an auction.
    Brodcast to [user_lists] users
    """
    
    if instance:
        if update_fields is None:
            """
            Not notified for updates
            """
            x=instance.user
            print(instance)
            print(x)
            user_lists=get_users_auction(x)
            
            for u in user_lists:
                Notification.objects.create(
                    receiver=u,
                    other_user=None,
                    auction=instance,
                    bid=None,
                    is_like=False
                )
            print("user x created an auction Brodcast to [user_lists] users")


def like(sender, instance, action, pk_set, **kwargs):
    """
    Signal created when user y likes the auction of user x.
    for optimization:
        . put text in DB, get faster data
        . or process msgs later but get it slow(better since ajax is there!!)
    
    Note this is for (Auction.upvotes.through) only. Auction.downvotes.through not done(not needed).
    """
    if instance:
        msg=""
        y = []  
    
        for k in pk_set:
            y = User.objects.get(id=k)
        
        x = instance.user 
        
        db_entry=x.bids_alert.filter(user=x,other_user=y,auction=instance, is_like=True)
        if action == "post_add":
            if db_entry.exists():
                num_of_likes=instance.upvotes.all().count()
                if(num_of_likes>0 and num_of_likes%3 == 0):
                    """ update after every 3 users are added(optimization)"""
                    username_list = ""
                    for notes_user in instance.upotes.all()[0:2]:
                        if not notes_user == x:
                            username_list += notes_user.username + ","
                    remaining_likes = instance.likes.all().count() - 2
                    msg = (
                        username_list
                        + " and "
                        + str(remaining_likes)
                        + " others liked your post!"
                    )
                    db_entry.update(created=timezone.now())

            elif not x == y:  # avoid sailesh liked sailesh post.
                msg = y.username + " liked " + x.username + " post!"
                Notification.objects.create(
                    receiver=x,
                    other_user=y,
                    auction=instance,
                    is_like=True,
                )

        elif action == "post_remove":
            msg = y.username + " unliked " + instance.user.username + " post!"
            db_entry.delete()

        print(msg)
