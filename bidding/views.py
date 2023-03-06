from django.shortcuts import(
    render,
    get_object_or_404,
    redirect,
) 
    

from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib import messages


from django.template.loader import render_to_string
from django.http import(
    HttpResponse,
    JsonResponse,
) 
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from mechanism.auction import Auction
from mechanism.notification import Notification
from mechanism.bidding import Bid


from .forms import (
    BidForm,
)
# Create your views here.
    
#bids
class BidCreateView(LoginRequiredMixin,View):   
    template_name="bid/form/create.html"
    def post(self,request,*args,**kwargs):
        estate_ = get_object_or_404(Auction, id=request.POST.get("id"))
        bid_amount=request.POST.get("bid_amount")
        bid=BidForm(bid_amount)
        if(bid.is_valid()):
            if(estate_.is_new_bid_okay(bidder=self.request.user,bid_amount=bid_amount) is False):
                #todo
                return JsonResponse({"form": html,"err":f"Bid creation Error. Enter amount bigger than {50}"}) 
            bid.save(commit=False)
            bid.auction=estate_
            bid.user=self.request.user
            bid.save()

            bid.bid_created_alert()
        
        context = {
        "bid_form":bid,
        
        }
        
        html = render_to_string(self.template_name, context, request=request)
        return JsonResponse({"form": html})



class BidUpdateView(View):
    template_name='bid/menu.html'
    
    def post(self,request,*args,**kwargs):
        bid = get_object_or_404(Bid, id=request.POST.get("id"))
        bid_amount=request.POST.get("bid_amount")
        err=None
        if(bid.auction.is_new_bid_okay(bidder=self.request.user,bid_amount=bid_amount)):
            if(bid.user is self.request.user):
                bid.update(bid_amount=bid_amount)
        else:
            err="Please enter valid bid amount "
        context = {
            "auction":bid.auction,
            "bid_form":BidForm(),        
        }
        
        html = render_to_string(self.template_name, context, request=request)
        return JsonResponse({"form": html})


    
    
class BidDeleteView(View):
    template_name="bid/list.html"
    def post(self,request,*args,**kwargs):
        bid = get_object_or_404(Bid, id=request.POST.get("id"))
        print(bid)
        context={}
        html = render_to_string(self.template_name, context, request=request)
        if(bid.user == self.request.user):
            bid.delete()
            messages.success(self.request,"Bid deleted successfully!")
            return JsonResponse({"form": html})
        
        #return JsonResponse({"form":html})
        


class BidPendingList(View):
    context_object_name="bids"
    template_name='bid/list.html'

    def get(self,request,*args,**kwargs):
        context=self.get_context_data()
    
        html = render_to_string(self.template_name, context, request=request)
        return JsonResponse({"form": html})


    def get_queryset(self):
        user=self.request.user
        bids=Bid.objects.filter(bidder=user)
        return bids
    
    def get_context_data(self):
        context={}
        qs=self.get_queryset()
        context[self.context_object_name]=qs
        return context

class BidHandleView(LoginRequiredMixin,View):
    def handle_silently(self):
        return JsonResponse({})
    def post(self, request, *args, **kwargs):
        intent=request.POST.get('intent')
        id_=request.POST.get('id')
        print("asa",id_)
        amount=request.POST.get('bid_amount')
        auction=get_object_or_404(Auction,id=id_)

        has_bid=True

        if(auction.user== request.user):
            return self.handle_silently()
        
        bid_html=None
        
        

        db_entry=Bid.objects.filter(auction=auction,bidder=request.user)
        if(intent== '0'):
            #add bid
            if(db_entry.exists()):
                print("already")
                self.handle_silently()
            else:
                db_entry=Bid.objects.create(auction=auction,bidder=request.user,bid_amount=amount)
                print("new")
                
        else:
            if( not db_entry.exists()):
                print("no entry")
                self.handle_silently()
            
            db_entry=db_entry.first()
            if(intent== '1'):
                #modify bid
                print("change")
                db_entry.bid_amount=amount
                db_entry.save()
                
            elif(intent== '2'):
                #delete bid
                db_entry.delete()
                has_bid=False
                print("del")
        
        if(intent=="0" or intent=="1"):
            bid_list=auction.get_bids_by_order()
            bid_html=render_to_string('bid/list.html',context={'bids':bid_list},request=request)

        bid_form=BidForm(initial={'bid_amount':amount})
        context={
            "auction":auction,
            "has_bid":has_bid,
            "bid_form":bid_form,
            "user":auction.user,
        }
        
        html=render_to_string('bid/menu.html',context=context,request=request)

        return JsonResponse({'html':html,'bid_list':bid_html,})

