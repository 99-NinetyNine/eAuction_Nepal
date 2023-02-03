from django.urls import reverse_lazy
from django.views import generic
from django.template.loader import render_to_string
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.db.models import Q
from django.http import(
        HttpResponse,
        JsonResponse,
) 
from django.contrib import messages
from .forms import (
    BidUserCreationForm,
    RatingForm,
)

from .models import BidUser,Rating
from auctions.models import Estate
from auctions.utils import (
    get_auction_query_set,
    is_ajax,
)

class SignUp(generic.CreateView):
    form_class = BidUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/user_signup_form.html'

class ProfileDetailView(generic.ListView):
    model=BidUser
    context_object_name="auctions"
    dest_user=None

    template_name='users/profile_view.html'

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        self.dest_user=get_object_or_404(BidUser,id=pk)
        estates=Estate.objects.filter(user=self.dest_user)
        return get_auction_query_set(estates,self.request)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['user'] = self.dest_user
        
        return context


    
class ProfileEditView(generic.UpdateView):
    model=BidUser
    fields=[
        'first_name',
        'last_name',
        'phone_num',
        'profile_pic',
        'bio',
    ]
    template_name="users/profile_change.html"

    def get_object(self):
        return BidUser.objects.get(user=self.request.user)

def RateUser(request):
    context_object_name="rating_form"
    
    context={}
    pk=request.GET.get('to_user_id')
    if(pk is None):
        pk=request.POST.get('to_user_id')
    
    user=get_object_or_404(BidUser,id=pk)   
    common_query=Rating.objects.filter(from_user=request.user,to_user=user)
    
    if(request.method=='GET'):
        does_exist_query=common_query
        rating='5'
        if(does_exist_query.exists()):
            rating=does_exist_query.first().rating
        form=RatingForm(initial={'rating':rating})
        context[context_object_name]=form
        
        
    else:
        rating=request.POST.get('rating')
        form=RatingForm(request.POST)
        if (not request.user == user and form.is_valid()):
            is_change_rate=common_query
            if(is_change_rate.exists()):
                instance=is_change_rate.first()
                if(rating=='0' or rating == 0):
                    instance.delete()
                else:
                    Rating.objects.filter(id=instance.id).update(rating=rating)

            else:
                form=form.save(commit=False)
                form.rating=rating
                form.from_user=request.user
                form.to_user=user
                form.save()
            messages.success(request,"Thanks for your rating!")
            context["rating"]=user.my_ratings()
            
    context['user']=user
    x=user.my_ratings()
    print(x)
    if(is_ajax(request)):
        html=render_to_string("users/rating_form.html",context=context,request=request)
        return JsonResponse({"form":html,"rating_value":x,})

    




class VerifyPhone(generic.CreateView):
    model=BidUser

    template_name='users/verify_phone.html'

    fields=[
        'phone_verified',
    ]


class AccountSettingView(generic.TemplateView):
    template_name="users/account_setting.html"

class SearchUser(generic.View):
    template_name="users/search_results.html"
    context_object_name="users"
    search_key=None
    def get(self,request):
        
        self.search_key=request.GET.get("query")
    
        context=self.get_context_data()
        
        if(is_ajax(self.request)):
            html=render_to_string(self.template_name,context=context,request=self.request)
            return JsonResponse({"json_data":html,})

    def get_queryset(self):
        users = None
        query=self.search_key
        if query:
            users = BidUser.objects.filter(
                Q(username__icontains=query)
                | Q(username__contains=query)
                | Q(username__startswith=query)
                | Q(username__endswith=query)
                | Q(first_name__icontains=query)
                | Q(first_name__contains=query)
                | Q(first_name__startswith=query)
                | Q(first_name__endswith=query)
                | Q(last_name__icontains=query)
                | Q(last_name__contains=query)
                | Q(last_name__startswith=query)
                | Q(last_name__endswith=query)
            )
        return users

    def get_context_data(self):
        context={
            self.context_object_name:self.get_queryset(),
        }
        return context