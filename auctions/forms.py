from django import forms
from mechanism.auction import Auction,AuctionImage
from mechanism.notification import Notification


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "youtube",
            "price_min_value",
            "price_max_value",
            "expiry_date",

        ]

        labels = {
            "title": "Add Title",
            "description":"Add description eg.4 aana ",
            "price_min_value":"Minimun Price:",
            "price_max_value":"Maximum price",
            "expiry_date":"Choose expiry date:",

        }

    


