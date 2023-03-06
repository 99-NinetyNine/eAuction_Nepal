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


class InitialBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "auction",
            "bail_trn_id",           

        ]

        labels = {
            "bail_trn_id": "Enter deposit id (10% of amount)",
        }

class FinalBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "auction",
            "remaining_trn_id",           

        ]

        labels = {
            "remaining_trn_id": "Enter deposit id (90% of amount)",
        }

