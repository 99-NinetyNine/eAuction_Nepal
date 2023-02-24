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

from mechanism.auction import Auction,AuctionImage
from mechanism.notification import Notification
from mechanism.bidding import Bid

#notification alerts
class ListAlertsView(LoginRequiredMixin,ListView):
    model=Notification
    context_object_name="notifications"
    template_name='_notification_list.html'
    #object_list=None
    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        context = super().get_context_data(object_list=queryset)
    
        html = render_to_string("_notification_list.html", context, request=request)
        return JsonResponse({"form": html})
        
        

    def get_queryset(self,**kwargs):
        
        """
        list of ["q==notification query","msg==customized"]
        """
        query_set=Notification.objects.filter(receiver=self.request.user)
        
        res=[]
        for q in query_set:
            t=[]
            is_like=False
            is_auction_notice=False
            is_bid_notice=False
            is_checked=False
            msg=""
            is_checked=q.is_checked

            if(q.is_like):
                is_like=True
                username_list = ""
                auction=q.auction
                num_of_likes=auction.upvotes.all().count()
                if(num_of_likes>0 and num_of_likes%3 == 0):
                
                    for voter in auction.upvotes.all()[0:2]:
                        if not notes_user == self.request.user:
                            username_list += notes_user.username + ","
                    remaining_likes = auction.upvotes.all().count() - 2
                    msg = (
                        username_list
                        + " and "
                        + str(remaining_likes)
                        + " others upvoted your auction!"
                    )
                else:
                    if(auction.user != self.request.user ):
                        msg = q.user.username + " liked " + " your auction!"


            
            elif(q.auction and not q.bid):
                """auction notice"""
                is_auction_notice=True
                msg=q.auction.user.username+"posted an auction. "


            elif(q.bid and q.auction):
                """is_bid_notice"""

                is_bid_notice=True
                msg=q.other_user.username +" has put bid on your auction "+q.auction.title
            
            t=[q,is_like,is_auction_notice,is_bid_notice,msg,is_checked]
            res.append(t)
        return res


        
class ListHandleView(LoginRequiredMixin,View):
    
    def post(self, request, *args, **kwargs):
        intent=request.POST.get('intent')
        note_id=request.POST.get('id')
        note=None
        user=None
        if(intent!=2):
            note=get_object_or_404(Notification,id=note_id)
            if not note.user==request.user:
                return JsonResponse({});
        if(intent==2):
            user=get_object_or_404(User,id=note_id)
            if not user==request.user:
                return JsonResponse({});

        if(intent=='0'):
            #checked
            if(not note.is_checked):
                note.is_checked=True
                note.save()
                print("yi")


        
        elif(intent=='1'):
            #delete
            note.delete()
            

        elif(intent=='2'):
            #clear
            user.bids_alert.all().delete()

        return JsonResponse({});

