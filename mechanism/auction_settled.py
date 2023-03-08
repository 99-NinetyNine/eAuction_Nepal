from django.db import models

from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings

import datetime
import uuid
import random

from mechanism.users import User


from mechanism.auction import Auction


class SettledAuction(models.Model):
    id= models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auction=models.OneToOneField(Auction,on_delete=models.CASCADE,related_name="settled")
    winner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="won")



    def __str__(self):
        return f"auction {str(self.auction.id)[0:4]},finnnnnnnallllly setttled  winner={self.winner.username}"
