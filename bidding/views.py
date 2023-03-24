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

from django.http import Http404, HttpResponseRedirect
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
    BidDeleteForm,
    InitialPayForm,
    FinalPayForm,
)
class PayFinalView(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        
        form=FinalPayForm(self.request.POST)
        if form.is_valid():
            if form.save(bidder=self.request.user):
                print("valid...")
                messages.add_message(self.request, messages.SUCCESS, "Your deposit ID has been received. Thanks for completing the process.")
                return HttpResponseRedirect(form.auction.get_absolute_url())

        error=form.get_err_msg()
        print(error)
        messages.add_message(self.request, messages.ERROR, error)
        if form.auction:
            return HttpResponseRedirect(form.auction.get_absolute_url())
        
        return HttpResponseRedirect(reverse("home"))

    
pay_final_view=PayFinalView.as_view()



class PayInitialView(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form=InitialPayForm(self.request.POST)
        if form.is_valid():
            form.save(bidder=self.request.user)
            messages.add_message(self.request, messages.ERROR, "Your deposit ID has been received. You can now start bidding.")
            return HttpResponseRedirect(form.auction.get_absolute_url())
        print(form)
        print("we are at rror")
        error=form.get_err_msg()
        messages.add_message(self.request, messages.ERROR, error)
        return HttpResponseRedirect(reverse("home"))

pay_initial_view=PayInitialView.as_view()


    


#bids
class BidCreateView(LoginRequiredMixin,View):   
    
    def post(self,request,*args,**kwargs):
        form=BidForm(self.request.POST)

        if(form.is_valid()):
            bid=form.save(bidder=self.request.user)
            if(bid):
                messages.add_message(self.request, messages.ERROR, "Your bid is placed.")
                return HttpResponseRedirect(form.auction.get_absolute_url())
            else:
                messages.add_message(self.request, messages.ERROR, "We couldnot place your bid.")
                return HttpResponseRedirect(form.auction.get_absolute_url())

            
        
        error=form.get_err_msg()
        messages.add_message(self.request, messages.ERROR, error)
        if form.auction:
            return HttpResponseRedirect(form.auction.get_absolute_url())
        
        return HttpResponseRedirect(reverse("home"))


class BidUpdateView(LoginRequiredMixin,View):
    
    def post(self,*args,**kwargs):
        form=BidForm(self.request.POST)
        if(form.is_valid()):
            bid=form.save(bidder=self.request.user,commit=True)
            return HttpResponseRedirect(form.auction.get_absolute_url())
    
        error=form.get_err_msg()
        messages.add_message(self.request, messages.ERROR, error)

        return HttpResponseRedirect(reverse("home"))


class BidDeleteView(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form=BidDeleteForm(self.request.POST)
        if(form.is_valid() and form.delete(self.request.user)):
            messages.add_message(self.request, messages.SUCCESS, "The bid is deleted.")
            return HttpResponseRedirect(form.auction.get_absolute_url())
        else:
            error=form.get_err_msg()
            messages.add_message(self.request, messages.ERROR, error)
            if form.auction:
                return HttpResponseRedirect(form.auction.get_absolute_url())
            
        
        return HttpResponseRedirect(reverse("home"))







class BidPendingList(View):
    context_object_name="bids"
    template_name='pages/my_bids.html'

    def get(self,request,*args,**kwargs):
        context=self.get_context_data()
        return render(self.request,self.template_name,context)

        ##old
        html = render_to_string(self.template_name, context, request=request)
        return JsonResponse({"form": html})


    def get_queryset(self):
        user=self.request.user
        bids=Bid.objects.filter(bidder=user)
        return bids
    
    def get_context_data(self):
        from mechanism.bidding import Bid
        all_bids=Bid.objects.filter(bidder=self.request.user)
        running_bids=[]
        for bid in all_bids:
            if bid.auction.exists_in_live_bucket():
                running_bids.append(bid)
        
        from mechanism.auction_settled import SettledAuction
        won_bids=SettledAuction.objects.filter(winner=self.request.user)
        
        
        context={
            "history":all_bids,
            "running":running_bids,
            "won":won_bids,
        }
        return context

class BidHandleView(LoginRequiredMixin,View):
    ##my work going to vain
    #so please learn soething useful first then only code.
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

