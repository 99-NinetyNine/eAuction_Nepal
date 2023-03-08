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


from django.contrib.auth import get_user_model
User=get_user_model()

from mechanism.models import Rating
from mechanism.auction import Auction
from mechanism.notification import Notification
from mechanism.bidding import Bid

from django.views import View
from .forms import (
    RatingForm,
)


class ContactView(View):
    def get(self,*a,**kw):
        return render(self.request,"pages/contact.html",{})

contact_view=ContactView.as_view()


class ProfileDetailView(LoginRequiredMixin,View):
    
    template_name='pages/profile.html'

    def get(self,*a,**k):
        return render(self,self.template_name,{})


    
class ProfileEditView(generic.UpdateView):
    model=User
    fields=[
        'first_name',
        'last_name',
        'phone_num',
        'profile_pic',
        'bio',
    ]
    template_name="pages/profile_change.html"

    def get_object(self):
        return User.objects.get(id=self.request.user.id)



def RateUser(request):
    context_object_name="rating_form"
    
    context={}
    pk=request.GET.get('to_user_id')
    if(pk is None):
        pk=request.POST.get('to_user_id')
    
    user=get_object_or_404(User,id=pk)   
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
    
    html=render_to_string("pages/rating_form.html",context=context,request=request)
    return JsonResponse({"form":html,"rating_value":x,})

    




class VerifyPhone(generic.CreateView):
    model=User

    template_name='pages/verify_phone.html'

    fields=[
        'phone_verified',
    ]



class SearchUser(generic.View):
    template_name="pages/search_results.html"
    context_object_name="users"
    search_key=None
    def get(self,request):
        
        self.search_key=request.GET.get("query")
    
        context=self.get_context_data()
        

        html=render_to_string(self.template_name,context=context,request=self.request)
        return JsonResponse({"json_data":html,})

    def get_queryset(self):
        users = None
        query=self.search_key
        if query:
            users = User.objects.filter(
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

