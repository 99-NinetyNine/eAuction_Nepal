from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class BidUser(AbstractUser):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    profile_pic= models.ImageField(default="default.jpg", upload_to="ProfileImages/")
    phone_num=models.PositiveBigIntegerField(null=True,blank=True,unique=True)
    bio=models.CharField(max_length=100,blank=False)
    latitude=models.CharField(blank=False)
    longitude=models.CharField(blank=False)
    phone_verified=models.BooleanField(default=False)
    

    
    def has_verified_phone(self):
        return self.phone_verified

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.id)])

class Rating(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    from_user=models.ForeignKey(BidUser,on_delete=models.cascade)
    to_user=models.ForeignKey(BidUser,on_delete=models.cascade)
    
    #useful for ai..show those users who u rated max
    RATING_CHOICES= [
        ('0','Poor'),
        ('1','Satisfactory'),
        ('2','Good'),
        ('3','Better'),
        ('4','Excellent'),
    ]
    rating=models.CharField(
        max_length=1,
        choices=RATING_CHOICES,
        default='0',
    )

    def my_ratings(self):
        pass
