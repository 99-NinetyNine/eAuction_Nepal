from django import forms 
from .models import (
    Estate,
    EstateImage,
    Bids,
)


class EstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = [
            "title",
            "description",
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


class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = [
            "bid_amount",           

        ]

        labels = {
            "bid_amount": "Enter bid amount(within range)",
        }
    


