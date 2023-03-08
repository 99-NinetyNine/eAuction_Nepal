from django import forms
from django.core.exceptions import ValidationError

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
            "open_close",
            "price_min_value",
            "price_max_value",
            "expiry_date",
            "thumbnail",
            
            "pdf",
            

        ]

        labels = {
            "title"                 :       "Enter title of auction:",
            "description"           :       "Enter description eg.4 aana ",
            "price_min_value"       :       "Enter starting bidding amount:",
            "price_max_value"       :       "Enter maximum amount",
            "youtube"               :       "Enter youtube video URL",
            "thumbnail"             :       "Enter thumbnail of auction",
            "pdf"                   :       "Enter pdf of notice",
            "open_close"            :       "Mark the checkbox, If auction is of Type -> Open",
            "expiry_date"           :       "Enter date when auction closes:",

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
    



class OtpFormForDisclose(forms.Form):
    ##admin enter their otp, we check their input, we process haha.
    auction=forms.UUIDField(widget = forms.HiddenInput())
    otp=forms.CharField(max_length=15,label="Dear Admin, please enter OTP here")

    
    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")

        try:
            self.auction=Auction.objects.get(id=auction)
        except Exception as e:
            raise ValidationError("Auction is invalid")
        
        if(not self.auction.exists_in_admin_waiting_bucket()):
            raise ValidationError(f"The auction is not in admin waiting phase.")


    
    def handle_otp(self,some_admin):
        ##my own haha
        try:
            if(self.auction.disclosed_by_admins()):
                raise ValidationError(f"Why are you entering otp, when no need be??")

            if(self.auction.check_otp_for_admins(admin=some_admin,some_otp=self.cleaned_data.get("otp"))):
                raise ValidationError(f"Oh no, You have entered wrong otp, we don't accept that.")
            #self.auction.admin

            if(not self.auction.some_admin_entered_otp()):
                raise ValidationError(f"Oh no, you maynot be admin, please fix the bug...")
            
            self.auction.push_to_not_settled_bucket()
        except ValidationError as v:
            self.add_error("auction",v)
            return False
        except Exception as e:
            print(e)
            return False
            
        return True
        
    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m

class Testt(forms.Form):
    a=forms.CharField(max_length=2)

    def some_random(self):
        try:
            
            raise ValidationError("hahaha i am idoiit")
        except ValidationError as v:
            self.add_error('a', v)
            return False
    