from django import forms
from mechanism.auction import Auction
from mechanism.notification import Notification

from django.contrib.auth import get_user_model
User=get_user_model()

class SuperAdminLoginForm(forms.Form):
    otp=forms.CharField(max_length=10)

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "youtube",
            "thumbnail",
            "price_min_value",
            "price_max_value",
            "expiry_date",
            "pdf",

        ]

        labels = {
            "title": "Add Title",
            "description":"Add description eg.4 aana ",
            "price_min_value":"Minimun Price:",
            "price_max_value":"Maximum price",
            "expiry_date":"Choose expiry date:",

        }
    def clean_youtube(value):
        import re

        print("cleaning")
        # The YouTube video link
        link = "https://www.youtube.com/watch?v=4vbDFu0PUew"

        # Extract the video ID using regular expression
        match = re.search(r"v=(\w+)", link)

        if match:
            video_id = match.group(1)
            return video_id
        return value
    


