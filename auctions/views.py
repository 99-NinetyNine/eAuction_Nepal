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
from django.forms import modelformset_factory
from django.db.models import Q

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


from bidding.forms import BidForm
from .forms import (
    AuctionForm,
)

INDEX_CONTEXT_NAME="auctions"

        

#from mechanism.trigger import hello

from celery import shared_task


@shared_task()
def hello_dodo(x):
    print("beat beat",x)

import random
def testy_od(re):
    hello_dodo.delay("hi")
    return render(re,"_auction.html",{"msg":"doing something by celery"})

def testy(re):
    return render(re,"need.html",{"msg":"doing something by celery"})


from pprint import pprint
class HomeView(LoginRequiredMixin,ListView):
    model=Auction
    template_name='_index.html'

    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        qs=Auction.query.for_index_page()
        
        context["newly_listed"],context["others"]   =   qs
        
        return context
        
    

def AuctionCreate(request):
    if request.method == "POST":
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()
            
            auction.auction_created_alert()
            messages.success(request, "Post has been successfully created.")
            return redirect("home")
        
        else:
            print(form.errors)
            messages.success(request, "Auction has not created.")
            return render(request, "auction/form/create.html", {"auction_create_form":form,})

    form=AuctionForm()
    return render(request, "auction/form/create.html", {"auction_create_form":form,})

def AuctionEdit(request, pk):
    auction = get_object_or_404(Auction, id=pk)
    if auction.user != request.user:
        raise Http404()
    
    if request.method == "POST":
        form = AuctionForm(request.POST or None, instance=auction)
        if form.is_valid():
            form.save()
            messages.success(request, "Auction has been successfully updated!")
            return HttpResponseRedirect(auction.get_absolute_url())
    else:
        form = AuctionForm(instance=auction)
    context = {
        "form": form,
        "auction": auction,
    }
    return render(request, "auction/form/edit.html", context)


    
class AuctionDeleteView(DeleteView):
    model=Auction
    context_object_name="auction"
    template_name='auction/auction_delete_form.html'

    def get_success_url(self):
        return reverse_lazy('profile_view',args=[self.request.user.id])

class AuctionDetailView(View):
    context_object_name="single_auction"
    template_name='auction/detail.html'
    pk=None
    auction=None
    def get(self,*args,**kwargs):

        context=self.get_context_data()
        return render(self.request,self.template_name,context)

    def get_object(self):
        self.pk=self.kwargs.get('pk')
        self.auction=get_object_or_404(Auction,id=self.pk)
        return Auction.query.get_serialized_query_set(self.auction, self.request,True)
    def get_bid_form(self):
        db_entry=self.auction.bids.filter(bidder=self.request.user)
        has_bid=False
        form=None
        if(db_entry.exists()):
            has_bid=True
            form=BidForm(initial={'bid_amount':db_entry[0].bid_amount})
        else:
            has_bid=False
            form=BidForm()
        return has_bid,form

    def get_context_data(self):
        context={}
        context[self.context_object_name]=self.get_object()
        
        bids=self.auction.get_bids_by_order()
        
        context["detail_view"]=True
        context["bids"]=bids
        context["auction"]=self.auction
        has_bid,form=self.get_bid_form()
        context["has_bid"]=has_bid
        context["bid_form"]=form
        

        return context
    
    
    
class NewAuctionDetailView(View):
    template_name='auction/detail.html'
    pk=None
    auction=None
    
    bidder_deposited_ten_percent =False
    bidder_has_bid = False
    bidder_won=False
    bidder_paid_ninty_percent=False
    seven_days_since_won_and_not_paid=False

    did_he_bid=False
    is_he_winner=True
    
    def get(self,*args,**kwargs):


        self.pk=self.kwargs.get('pk')
        self.auction=get_object_or_404(Auction,id=self.pk)
        
        self.seeing_by_admins       =   False
        self.seeing_by_bidder       =   True
        self.seeing_by_anonynous    =   False
        ##
        self.of_type_open           =   self.auction.is_type_open()
        ##
        self.bidding_not_started    =   self.auction.bidding_not_started()
        self.in_bidding_season      =   self.auction.in_bidding_season()
        self.bidding_season_closed  =   self.auction.bidding_season_closed()
        self.disclosed_by_admins    =   self.auction.disclosed_by_admins()

        if(not self.request.user.is_authenticated):
            
            self.handle_anonymous_user()

        else:
            if(self.request.user.is_one_of_admins()):
                
                self.handle_admins()
            
            else:
                self.handle_bidder()


        #common data, max price,len(bidders),etc
        return render(self.request,self.template_name,self.get_context_data())
    
    def handle_anonymous_user(self):
        self.seeing_by_anonynous=True


    def handle_admins(self):
        self.seeing_by_admins=True


    def handle_bidder(self):
        self.seeing_by_bidder=True
        if(self.bidding_not_started or self.in_bidding_season):
            self.bidder_deposited_ten_percent=self.auction.bidder_paid_initial(self.request.user)
        
        if(self.disclosed_by_admins and self.request.user==self.auction.get_bid_winner()):
            self.is_he_winner=True    
    
        if self.bidder_deposited_ten_percent:
            self.did_he_bid=self.auction.is_he_bidder(self.request.user)
            if self.did_he_bid:
                self.amount_he_bid=self.auction.get_amount_he_bid(self.request.user)
        

    def get_context_data(self):
        context={}
        if(self.of_type_open or self.disclosed_by_admins):
            bids=self.auction.get_bids_by_order()
        else:
            bids=[]
        
        context["detail_view"]=True
        context["bids"]=bids
        
        context["seeing_by_admins"]                     =       self.seeing_by_admins
        context["seeing_by_bidder"]                     =       self.seeing_by_bidder
        context["seeing_by_anonynous"]                  =       self.seeing_by_anonynous
        context["of_type_open"]                         =       self.of_type_open
        context["bidding_not_started"]                  =       self.bidding_not_started
        context["in_bidding_season"]                    =       self.in_bidding_season
        context["bidding_season_closed"]                =       self.bidding_season_closed
        context["disclosed_by_admins"]                  =       self.disclosed_by_admins
        context["bidder_deposited_ten_percent"]         =       self.bidder_deposited_ten_percent
        context["bidder_has_bid"]                       =       self.bidder_has_bid
        context["bidder_won"]                           =       self.bidder_won
        context["bidder_paid_ninty_percent"]            =       self.bidder_paid_ninty_percent
        context["seven_days_since_won_and_not_paid"]    =       self.seven_days_since_won_and_not_paid
        context["did_he_bid"]                           =       self.did_he_bid
        context["is_he_winner"]                         =       self.is_he_winner
        return context



        
@login_required
def LikeAuction(request):
    auction = get_object_or_404(Auction, id=request.POST.get("id"))
    is_liked = False
    is_disliked=False

    intent=request.POST.get("intent")
    
    #like btn
    if( intent== "0"):
        if auction.upvotes.filter(id=request.user.id).exists():
            auction.upvotes.remove(request.user)
        else:
            auction.upvotes.add(request.user)
            is_liked=True
            auction.new_like_notification(liker=request.user)
            
            if auction.downvotes.filter(id=request.user.id).exists():
                auction.downvotes.remove(request.user)

    elif(intent=="1"):
        if auction.downvotes.filter(id=request.user.id).exists():
            auction.downvotes.remove(request.user)
        else:
            auction.downvotes.add(request.user)
            is_disliked=True
            
            if auction.upvotes.filter(id=request.user.id).exists():
                auction.upvotes.remove(request.user)


    context = {
        "auction": auction,
        "is_liked": is_liked,
        "is_disliked":is_disliked,
        
    }
   
    
    like_html = render_to_string("auction/bottom/thumb_up.html", context=context, request=request)
    dislike_html = render_to_string("auction/bottom/thumb_down.html", context=context, request=request)
    
    json_data={
        "like_html": like_html,
        "dislike_html": dislike_html,

    }
    return JsonResponse(json_data)





def FavouriteAuction(request):
    auction = get_object_or_404(Auction, id=request.POST.get("id"))
    is_fav = False
    

    if auction.favourite.filter(id=request.user.id).exists():
        auction.favourite.remove(request.user)
    else:
        auction.favourite.add(request.user)
        is_fav = True
    context = {
        "auction": auction,
        "is_favourite": is_fav,
    }

    html = render_to_string("auction/bottom/fav.html", context, request=request)
    return JsonResponse({"form": html})

class FavouriteAuctionList(ListView):
    template_name="_index.html"
    context_object_name=INDEX_CONTEXT_NAME
    def get_queryset(self):
        favourite_posts = self.request.user.favourites.all()
        return Auction.query.get_serialized_query_set(favourite_posts, self.request)