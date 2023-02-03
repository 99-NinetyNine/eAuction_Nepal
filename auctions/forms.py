from django import forms 
from location_field.forms.plain import PlainLocationField
from .models import (
    Estate,
    EstateImage,
    Bids,
)
class Address(forms.Form):
    city = forms.CharField()
    location = PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')


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
    


