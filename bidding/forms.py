from django import forms 
from django.core.exceptions import ValidationError

from mechanism.bidding import Bid
from mechanism.auction import Auction


class BidDeleteForm(forms.Form):
    bid=forms.UUIDField(widget = forms.HiddenInput())

    def clean(self):
        cleaned_data=super().clean()
        bid=cleaned_data.get("bid")
        try:
            self.bid=Bid.objects.get(id=bid)
        except Exception as e:
            raise ValidationError("The bid is not found")

    def delete(self,some_user):
        try:
            if not self.bid.bidder==some_user:
                raise ValidationError("The bidder is not nice.")
            else:
                self.bid.delete()
            
        except ValidationError as v:
            self.add_error("bid",v)
            return False
        except Exception as e:
            print(e)
            return False
        


    

class BidForm(forms.Form):
    auction=forms.UUIDField(widget = forms.HiddenInput())
    bid_amount=forms.CharField(max_length=10,label="Enter bid amount(within range)")

    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")

        try:
            self.auction=Auction.objects.get(id=auction)
        except Exception as e:
            print(e)
            raise ValidationError("Auction is invalid")
        
        if(not self.auction.exists_in_live_bucket()):
            raise ValidationError(f"The auction is not in bidding phase.")
        
        
        if(self.auction.is_new_bid_okay(\
            bid_amount= cleaned_data.get("bid_amount"))):
            pass
        else:
            raise ValidationError(f"Bid amount is not valid. Your bid must be greater that or equal to {auction.get_highest_bidder().bid_amount}.")
        


    def save(self,bidder,commit=False):
        ##my own haha
        try:
            if(not auction.bidder_paid_initial(bidder)):
                raise ValidationError(f"Please  deposit 10% of starting price before bidding.")

            bid=Bid.objects.create(auction=self.auction,bidder=bidder,bid_amount=self.cleaned_data["bid_amount"])
            bid.save(commit=commit)
            return bid
        except ValidationError as v:
            self.add_error("auction",v)
            return False
        except Exception as e:
            print(e)
            return False
        
    
    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m
        

class InitialPayForm(forms.Form):
    auction         =   forms.UUIDField(widget = forms.HiddenInput())
    bail_trn_id     =   forms.CharField(max_length=100,label="Enter deposit id (10% of amount)")

    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")

        try:
            self.auction=Auction.objects.get(id=auction)
        except Exception as e:
            raise ValidationError("Auction is invalid")
        
        if(not self.auction.exists_in_live_bucket()):
            raise ValidationError(f"The auction is not in bidding phase.")

    
    def save(self,bidder,commit=False):
        ##my own haha
        try:
            if(self.auction.bidder_paid_initial(bidder)):
                raise ValidationError(f"Why are you paying again ??")

            bid=Bid.objects.create(auction=self.auction,bidder=bidder,bail_trn_id=self.cleaned_data["bail_trn_id"])
            bid.save(commit=commit)
            return bid

        except ValidationError as v:
            self.add_error("auction",v)
            return False
        except Exception as e:
            print(e)
            return False
        
    
    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m
    
    
class FinalPayForm(forms.Form):
    auction=forms.UUIDField(widget = forms.HiddenInput())
    remaining_trn_id     =   forms.CharField(max_length=100,label="Enter deposit id (10% of amount)")

    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")

        try:
            self.auction=Auction.objects.get(id=auction)
        except Exception as e:
            raise ValidationError("Auction is invalid")
        
        if(not self.auction.exists_in_not_settled_bucket()):
            raise ValidationError(f"The auction is not in settlement phase.")

    
    def save(self,bidder):
        ##my own haha
        try:
            if(self.auction.bidder_paid_remaining(bidder)):
                raise ValidationError(f"Why are you paying again ??")

            bid=self.auction.get_highest_bidder()
            
            if(bid.bidder != bidder):
                raise ValidationError(f"You are not winner, please let winner pay.")
            
            bid.mark_remaining_paid(txn=self.cleaned_data["remaining_trn_id"])

            self.auction.push_to_settled_bucket()
            
            ##may need to notify
            #todo
            
        
            return bid
        
        except ValidationError as v:
            self.add_error("auction",v)
            return False
        except Exception as e:
            print(e)
            return False
        
    
    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m