from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .models import Estate,EstateImage,Bids,Notification


#@login_required
def home(request):
    return HttpResponse("hello")

class AuctionCreateView(CreateView):
    model=Estate
    fields=[
        'title',
        'description',
        'location', 
        'hide_post',     
        'price_range',

    ]
    template_name='templates/auction_create_form.html'


    
class AuctionEditView(UpdateView):
    model=Estate
    fields=[
        'title',
        'description',
        'location', 
        'hide_post',     
        'price_range',


    ]

    template_name='templates/auction_update_form.html'

    
class AuctionDeleteView(DeleteView):
    model=Estate
    success_url=reverse_lazy('profile_view')
    template_name='templates/auction_delete_form.html'

class EstateDetailView(DetailView):
    model=Estate

    template_name='templates/auction_detail.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

    
class ImageLinkView(DetailView):

    model=ImageLink
    template_name='templates/auction_image_detail.html'

    
#bids
class BidCreateView(CreateView):
    model=Bid
    fields=[
        'bid_amount',
    ]
    template_name='templates/bid_create_form.html'


class BidUpdateView(UpdateView):
    model=Bid
    fields=[
        'bid_amount',
    ]
    template_name='templates/bid_update_form.html'
    
class BidDeleteView(DeleteView):
    model=Bid

    success_url=reverse_lazy('auction_detail',args=[self.Estate.id])

class BidDetailView(DetailView):
    model=Bid

    template_name='templates/bid_detail.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

    

#notification alerts
class ListAlertsView(ListView):
    model=Notification

    template_name='templates/notification_list.html'

    
class NotificationDetailView(DetailView):
    model=Notification
    template_name='templates/notification_detail.html'

