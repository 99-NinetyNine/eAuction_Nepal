from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator



from django.utils import timezone
import datetime

from django.conf import settings

from django.shortcuts import reverse

from PIL import Image

from location_field.models.plain import PlainLocationField


# class Place(models.Model):
#     city = models.CharField(max_length=100)
#     location = PlainLocationField(based_fields=['city'], zoom=7)

class Estate(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="estate")
    title=models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=200, blank=False)

    #location = models.OneToOneField(Place, on_delete=models.CASCADE)
    
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dislikes", blank=True)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favourites", blank=True)
    hide_post = models.BooleanField(default=False, blank=True)
    
    expiry_date=models.DateTimeField(default=timezone.now)  #put it 7 days later
    
    price_min_value= models.IntegerField(default=1)
    price_max_value=models.IntegerField(default=100)

    pub_date = models.DateTimeField(default=timezone.now)
        

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.user.username} property"

    def total_upvotes(self):
        return self.upvotes.count()

    def get_absolute_url(self):
        return reverse("estate_detail", args=[str(self.id)])

    def was_recent(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(seconds=30)


class EstateImage(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name="media")
    about = models.CharField(max_length=50, blank=True)
    photo = models.FileField(upload_to="EstateImages/", blank=True, null=True)
    is_photo = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.nature.user.username} gallery"
    def get_absolute_url(self):
        return reverse('image_link', args=[str(self.id)])

class Bids(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    estate=models.ForeignKey(Estate, on_delete=models.CASCADE,related_name="bids")
    bid_amount=models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('bid_detail', args=[str(self.id)])


class Notification(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="bids_alert", on_delete=models.CASCADE, default=None
    )
    auction = models.OneToOneField(Estate, on_delete=models.CASCADE, null=True)
    created=models.DateTimeField(default=timezone.now)    
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.auction.title
    def get_absolute_url(self):
        return reverse('notification_detail', args=[str(self.id)])
