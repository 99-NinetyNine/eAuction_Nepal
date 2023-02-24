from django import forms 
from mechanism.bidding import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "bid_amount",           

        ]

        labels = {
            "bid_amount": "Enter bid amount(within range)",
        }
