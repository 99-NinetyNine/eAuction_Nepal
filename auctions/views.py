from django.shortcuts import(
    render,
    get_object_or_404,
    redirect,
) 


from django.http import Http404, HttpResponseRedirect


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
    OtpFormForDisclose,
)

from bidding.forms import (
    BidDeleteForm,
    BidForm,
    InitialPayForm,
    FinalPayForm,
)

INDEX_CONTEXT_NAME="auctions"

        

#from mechanism.trigger import hello

from pprint import pprint
from celery import shared_task
import random


@shared_task()
def hello_dodo(x):
    print("beat beat",x)

def testy_od(re):
    hello_dodo.delay("hi")
    return render(re,"_auction.html",{"msg":"doing something by celery"})

def testy(re):
    return render(re,"need.html",{"msg":"doing something by celery"})

class DefaultView(View):
    def get(self,*args,**kwargs):
        pass
    def post(self,*args,**kwargs):
        pass

class AdminOtpView(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form=OtpFormForDisclose(self.request.POST)
        if form.is_valid():
            form.handle_otp()
            return HttpResponseRedirect(reverse(form.auction.get_absolute_url()))
        
        error=form.get_err_msg()
        messages.add_message(self.request, messages.ERROR, error)
        return HttpResponseRedirect(reverse("home"))

        
        


admin_otp_view=AdminOtpView.as_view()



class HomeView(View):
    
    newly_listed_auctions=None
    not_newly_listed_auctions=None
    auctions_inventory_incharge_created=None
    auctions_waiting_for_admin=None
    
    def get(self,*args,**kwargs):
        print(self.request.user.is_authenticated)
        
        if not self.request.user.is_authenticated:
            self.prepare_auctions_for_anonymous()
        elif self.request.user.is_inventory_incharge_officer():
            self.prepare_auctions_for_inventory_incharge()
        elif self.request.user.is_one_of_admins():
            self.prepare_auctions_for_one_of_admins()
        elif self.request.user.is_bidder():
            self.prepare_auctions_for_bidder()
        
        return render(self.request,"_index.html",self.get_context_data())
    

    def prepare_auctions_for_anonymous(self):
        self.newly_listed_auctions,self.not_newly_listed_auctions=Auction.query.for_index_page()

    def prepare_auctions_for_inventory_incharge(self):
        self.auctions_inventory_incharge_created=Auction.query.inventory_incharge_created(self.request.user)
    def prepare_auctions_for_one_of_admins(self):
        self.auctions_waiting_for_admin=Auction.query.waiting_for_admin(self.request.user)
    def prepare_auctions_for_bidder(self):
        self.newly_listed_auctions,self.not_newly_listed_auctions=Auction.query.for_index_page()
    
    def get_context_data(self,):
        context={}
        context["newly_listed_auctions"]                =   self.newly_listed_auctions
        context["not_newly_listed_auctions"]            =   self.not_newly_listed_auctions
        context["auctions_inventory_incharge_created"]  =   self.auctions_inventory_incharge_created
        context["auctions_waiting_for_admincontext"]    =   self.auctions_waiting_for_admin
        
        return context
    
    

def AuctionCreate(request):
    if(not request.user.is_inventory_incharge_officer()):
        return render(request,"auction/form/create.html", {"not_inventory_incharge":True,})
        
    if request.method == "POST":
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()
            
            auction.notify_that_auction_is_created()
            auction.push_to_live_bucket()
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
    
    did_he_bid=False
    is_he_winner=False
    
    bidder_paid_ninty_percent=False
    seven_days_since_won_and_not_paid=False

    adminA_entered_otp=False
    adminB_entered_otp=False
    adminC_entered_otp=False


    ##forms
    admin_otp_form=None

    bidder_paying_initial_form=None
    bidder_paying_remaining_form=None

    bid_bidding_form=None
    bid_deleting_form=None

    
    def get(self,*args,**kwargs):
        self.pk=self.kwargs.get('pk')
        self.auction=get_object_or_404(Auction,id=self.pk)
        
        self.seeing_by_admins       =   False
        self.seeing_by_bidder       =   False
        self.seeing_by_anonynous    =   False
        ##
        self.is_type_open           =   self.auction.is_type_open()
        ##doing this, cause we will having fun when in REACT if we send 
        #auction object and write auction.exists_in() 

        self.exists_in_dead_bucket              =   self.auction.exists_in_dead_bucket() #later manage this
        self.exists_in_live_bucket              =   self.auction.exists_in_live_bucket()
        self.exists_in_admin_waiting_bucket     =   self.auction.exists_in_admin_waiting_bucket()
        self.exists_in_not_settled_bucket       =   self.auction.exists_in_not_settled_bucket()
        self.exists_in_settled_bucket           =   self.auction.exists_in_settled_bucket()
        self.exists_in_re_schedule_bucket       =   self.auction.exists_in_re_schedule_bucket()
        
        if(self.exists_in_admin_waiting_bucket):
            self.adminA_entered_otp  =   self.auction.adminA_logged_in()
            self.adminB_entered_otp  =   self.auction.adminB_logged_in()
            self.adminC_entered_otp  =   self.auction.adminC_logged_in()
        
        if(not self.request.user.is_authenticated):
            
            self.handle_anonymous_user()

        elif(self.request.user.is_one_of_admins()):
            self.handle_admins()
                
        elif(self.request.user.is_bidder()):
            self.handle_bidder()
                
        else:
            self.handle_anonymous_user()


        #common data, max price,len(bidders),etc
        return render(self.request,self.template_name,self.get_context_data())
    
    def handle_anonymous_user(self):
        self.seeing_by_anonynous=True


    def handle_admins(self):
        self.seeing_by_admins=True
        if(self.exists_in_admin_waiting_bucket):
            self.admin_otp_form=OtpFormForDisclose(data={"auction":self.auction.id})



    def handle_bidder(self):
        self.seeing_by_bidder=True
        if(self.exists_in_dead_bucket or self.exists_in_live_bucket):
            if(self.auction.bidder_paid_initial(self.request.user)):
                self.bidder_deposited_ten_percent   =   True
            else:           
                self.bidder_paying_initial_form     =   InitialPayForm(data={'auction':str(self.auction.id)})


            if self.bidder_deposited_ten_percent:
                self.did_he_bid,self.amount_he_bid,bid_tuple=self.auction.does_he_have_bid(self.request.user)
                
                if self.did_he_bid:
                    self.bid_bidding_form=BidForm(data={"auction":self.auction.id,"bid_amount":self.amount_he_bid})
                    self.bid_deleting_form=BidDeleteForm(data={"bid":bid_tuple.id,})

                else:
                    self.bid_bidding_form=BidForm(data={"auction":self.auction.id,"bid_amount":0})
        
        if(self.exists_in_not_settled_bucket and self.request.user==self.auction.get_bid_winner()):
            self.is_he_winner=True
            self.bidder_paying_final_form     =   FinalPayForm(data={'auction':str(self.auction.id)})

    
        
        

    def get_context_data(self):
        context={}
        if(self.is_type_open or self.auction.exists_in_settled_bucket()):
            bids=self.auction.get_bids_by_order()
        else:
            bids=[]
        
        context["detail_view"]=True
        context["bids"]=bids
        
        context["seeing_by_admins"]                     =       self.seeing_by_admins
        context["seeing_by_bidder"]                     =       self.seeing_by_bidder
        context["seeing_by_anonynous"]                  =       self.seeing_by_anonynous
        context["is_type_open"]                         =       self.is_type_open
        context["exists_in_dead_bucket"]                =       self.exists_in_dead_bucket
        context["exists_in_live_bucket"]                =       self.exists_in_live_bucket
        context["exists_in_admin_waiting_bucket"]       =       self.exists_in_admin_waiting_bucket
        context["exists_in_not_settled_bucket"]         =       self.exists_in_not_settled_bucket
        context["exists_in_settled_bucket"]             =       self.exists_in_settled_bucket
        context["exists_in_re_schedule_bucket"]         =       self.exists_in_re_schedule_bucket
        context["adminA_entered_otp"]                   =       self.adminA_entered_otp
        context["adminB_entered_otp"]                   =       self.adminB_entered_otp
        context["adminC_entered_otp"]                   =       self.adminC_entered_otp
        context["bidder_deposited_ten_percent"]         =       self.bidder_deposited_ten_percent
        context["did_he_bid"]                           =       self.did_he_bid
        context["is_he_winner"]                         =       self.is_he_winner
        context["bidder_paid_ninty_percent"]            =       self.bidder_paid_ninty_percent
        context["seven_days_since_won_and_not_paid"]    =       self.seven_days_since_won_and_not_paid
        context["admin_otp_form"]                       =       self.admin_otp_form
        context["bidder_paying_initial_form"]           =       self.bidder_paying_initial_form
        context["bidder_paying_remaining_form"]         =       self.bidder_paying_remaining_form
        context["bid_bidding_form"]                     =       self.bid_bidding_form
        context["bid_deleting_form"]                    =       self.bid_deleting_form
        context["auction"]                              =       self.auction

        pprint(context)
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