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
            res.append("Notification ")
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

