from django.conf import settings

from .models import (
    Estate,
    EstateImage,
    Bids,
    Notification,
)
from users.models import(
    BidUser
)
from django.dispatch import receiver

from django.db.models.signals import (
    post_save,
    post_delete,
    m2m_changed,
)
from django.core.signals import request_finished

import django.dispatch
from django.utils import timezone

# custom class -boy :)
#index_view_done = django.dispatch.Signal(providing_args=["request",])


@receiver(m2m_changed, sender=Estate.upvotes.through)
def like(sender, instance, action, pk_set, **kwargs):
    """
    Signal created when user y likes the auction of user x.
    for optimization:
        . put text in DB, get faster data
        . or process msgs later but get it slow(better since ajax is there!!)
    
    Note this is for (Estate.upvotes.through) only. Estate.downvotes.through not done(not needed).
    """
    if instance:
        msg=""
        y = []  
    
        for k in pk_set:
            y = BidUser.objects.get(id=k)
        
        x = instance.user 
        
        db_entry=x.bids_alert.filter(user=x,other_user=y,estate=instance, is_like=True)
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
                    user=x,
                    other_user=y,
                    estate=instance,
                    is_like=True,
                )

        elif action == "post_remove":
            msg = y.username + " unliked " + instance.user.username + " post!"
            db_entry.delete()

        print(msg)

@receiver(post_save, sender=Estate)
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
                    user=u,
                    other_user=None,
                    estate=instance,
                    bid=None,
                    is_like=False
                )
            print("user x created an auction Brodcast to [user_lists] users")


@receiver(post_delete, sender=Estate)
def auction_delete_alert(sender, instance, **kwargs):
    if(instance):
        x=instance.user
        user_lists=get_users_auction(x)

        for u in user_lists:
            Notification.objects.get(
                    user=u,
                    other_user=None,
                    estate=instance,
                    bid=None,
                    is_like=False
                ).delete()

    print(instance.user.username, "deleted a auction!", instance.title)


def get_users_auction(user_not_needed):
    """
    Bunch of users to whom notification is to be sent. Can obtained by using AI(skills and ratings and past experience)

    """
    return BidUser.objects.exclude(id=user_not_needed.id)





@receiver(post_save, sender=Bids)
def bids_created_alert(sender, instance, **kwargs):
    if instance.user:
        
        x=instance.estate.user
        y=instance.user
        A=instance.estate

        if not x == y:
            """
            Not available option for modified operation so check once.
            """
            if not x.bids_alert.filter(
                other_user=y, bid=instance.id or None, is_like=False
            ).exists():
                Notification.objects.create(
                    user=x,
                    other_user=y,
                    estate=A,
                    bid=instance,
                    is_like=False,                    
                )


@receiver(post_delete, sender=Bids)
def bids_removed_alert(sender, instance, **kwargs):
    if instance:
        """
        remove that notifin which says
        x posted bid on auction y
        
        instance.estate.user.bid_list.filter(user_by=instance.user,bid=instance.id or None,is_like=False).delete()
        """

        
    

