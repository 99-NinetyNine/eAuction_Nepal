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


from .models import Estate,EstateImage,Bids,Notification
from .utils import (
    get_auction_query_set,
    is_ajax,
    get_bids_by_order,
    
)

from .forms import (
    EstateForm,
    BidForm,

)

INDEX_CONTEXT_NAME="auctions"

        


class HomeView(LoginRequiredMixin,ListView):
    model=Estate
    template_name='_index.html'
    context_object_name=INDEX_CONTEXT_NAME

    def get_queryset(self,**kwargs):
        query_set=super().get_queryset()
        return get_auction_query_set(query_set,self.request)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context
        
    

    

class AuctionCreateView(LoginRequiredMixin,CreateView):
    model=Estate
    fields=[
        'title',
        'description',
        'hide_post',     
        'price_min_value',
        'price_max_value',

    ]
    context_object_name="auction"

    template_name='auctions/auction_create_form.html'
    login_url='login'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def AuctionCreate(request):
    
    ImageFormset = modelformset_factory(
        EstateImage, fields=("about", "photo",),
    )
    if request.method == "POST":
        form = EstateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES)
        if form.is_valid() and formset.is_valid():
            estate = form.save(commit=False)
            estate.user = request.user
            estate.save()
            no_of_formset = 0
            no_of_error = 0
            for f in formset:
                try:
                    estateimage = EstateImage(
                        estate=estate,
                        about=f.cleaned_data.get("about"),
                        photo=f.cleaned_data.get("photo"),
                    )
                    
                    estateimage.save()
                    
                except Exception as e:
                    print("error @ formset",e)
                    if not estateimage:
                        no_of_error += 1

                no_of_formset += 1
            
            if no_of_formset == no_of_error:
                estate.delete()
                messages.success(request, "Post has not created.")
                return redirect("create_auction")

            messages.success(request, "Post has been successfully created.")
            return redirect("home")

    else:
        form=EstateForm()
        formset = ImageFormset(queryset=EstateImage.objects.none())
    return render(request, "auctions/auction_create_form.html", {"estate_form":form, "formset": formset,})

def AuctionEdit(request, pk):
    estate = get_object_or_404(Estate, id=pk)
    if estate.user != request.user:
        raise Http404()
    ImageFormset = modelformset_factory(
        EstateImage, fields=("about", "photo",), extra=4, max_num=4
    )
    if request.method == "POST":
        form = EstateForm(request.POST or None, instance=estate)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            data = EstateImage.objects.filter(estate=estate)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data["id"] is None:
                        photo = EstateImage(
                            estate=estate, photo=f.cleaned_data.get("photo")
                        )
                        photo.save()
                    elif f.cleaned_data["photo"] is False:
                        photo = EstateImage.objects.get(
                            id=request.POST.get("form-" + str(index) + "-id")
                        )
                        photo.delete()
                    else:
                        photo = EstateImage(
                            estate=estate, photo=f.cleaned_data.get("photo")
                        )
                        d = EstateImage.objects.get(id=data[index].id)
                        d.image = photo.photo
                        d.save()
            messages.success(request, "Post has been successfully updated!")
            return HttpResponseRedirect(estate.get_absolute_url())
    else:
        form = EstateForm(instance=estate)
        formset = ImageFormset(queryset=EstateImage.objects.filter(estate=estate))
    context = {
        "form": form,
        "estate": estate,
        "formset": formset,
    }
    return render(request, "auctions/auction_update_form.html", context)


    
class AuctionEditView(UpdateView):
    model=Estate
    fields=[
        'title',
        'description',
        'hide_post',     
        'price_min_value',
        'price_max_value',


    ]
    context_object_name="auction"

    template_name='auctions/auction_update_form.html'

    
class AuctionDeleteView(DeleteView):
    model=Estate
    context_object_name="auction"
    template_name='auctions/auction_delete_form.html'

    def get_success_url(self):
        return reverse_lazy('profile_view',args=[self.request.user.id])

class EstateDetailView(View):
    context_object_name="single_auction"
    template_name='auctions/auction_detail.html'
    pk=None
    auction=None
    def get(self,*args,**kwargs):

        context=self.get_context_data()
        return render(self.request,self.template_name,context)

    def get_object(self):
        self.pk=self.kwargs.get('pk')
        print(self.pk)
        self.auction=get_object_or_404(Estate,id=self.pk)
        return get_auction_query_set(self.auction, self.request,True)
    def get_bid_form(self):
        db_entry=self.auction.bids.filter(user=self.request.user)
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
        
        bids=get_bids_by_order(self.auction)
        
        context["detail_view"]=True
        context["bids"]=bids

        has_bid,form=self.get_bid_form()
        context["has_bid"]=has_bid
        context["bid_form"]=form
        

        return context
    
    
    

    
class ImageLinkView(DetailView):

    model=EstateImage
    template_name='auctions/auction_image_detail.html'

    
#bids
class BidCreateView(LoginRequiredMixin,View):   
    template_name="auctions/bid_create.html"
    def post(self,request,*args,**kwargs):
        estate_ = get_object_or_404(Estate, id=request.POST.get("id"))
        bid_amount=request.POST.get("bid_amount")
        bid=BidForm(bid_amount)
        if(bid.is_valid()):
            bid.save(commit=False)
            bid.estate=estate_
            bid.user=self.request.user
            bid.save()
        
        context = {
        "bid_form":bid,
        
        }
        
        if is_ajax(self.request):
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"form": html})
    




class BidUpdateView(View):
    template_name='auctions/bid_update_form.html'
    
    def post(self,request,*args,**kwargs):
        bid = get_object_or_404(Bids, id=request.POST.get("id"))
        bid_amount=request.POST.get("bid_amount")
        
        if(range_check(bid_amount,bid.estate.price_min_value,bid.estate.price_max_value)):
            if(bid.user is self.request.user):
                bid.update(bid_amount=bid_amount)
        
        context = {
        "bid_form":bid,        
        }
        
        if is_ajax(self.request):
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"form": html})
    
def range_check(bid,low,high):
    x= bid>=low and bid <=high
    return x

    
    
class BidDeleteView(View):
    template_name="auctions/bid_pending_lists.html"
    def post(self,request,*args,**kwargs):
        bid = get_object_or_404(Bids, id=request.POST.get("id"))
        print(bid)
        context={}
        html = render_to_string(self.template_name, context, request=request)
        if(bid.user == self.request.user):
                bid.delete()
                messages.success(self.request,"Bid deleted successfully!")
                if( is_ajax(self.request)):
                    return JsonResponse({"form": html})
        
        #return JsonResponse({"form":html})
        


class BidPendingList(View):
    context_object_name="bids"
    template_name='auctions/bid_pending_lists.html'

    def get(self,request,*args,**kwargs):
        context=self.get_context_data()
        if( is_ajax(self.request)):
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"form": html})

        return render(request,self.template_name,context)

    def get_queryset(self):
        user=self.request.user
        bids=Bids.objects.filter(user=user)
        return bids
    
    def get_context_data(self):
        context={}
        qs=self.get_queryset()
        context[self.context_object_name]=qs
        return context

    

#notification alerts
class ListAlertsView(LoginRequiredMixin,ListView):
    model=Notification
    context_object_name="notifications"
    template_name='_notification_list.html'
    #object_list=None
    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        context = super().get_context_data(object_list=queryset)
        if(is_ajax(request)):
            html = render_to_string("_notification_list.html", context, request=request)
            return JsonResponse({"form": html})
            
        

    def get_queryset(self,**kwargs):
        
        """
        list of ["q==notification query","msg==customized"]
        """
        query_set=Notification.objects.filter(user=self.request.user)
        
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
                estate=q.estate
                num_of_likes=estate.upvotes.all().count()
                if(num_of_likes>0 and num_of_likes%3 == 0):
                
                    for voter in estate.upvotes.all()[0:2]:
                        if not notes_user == self.request.user:
                            username_list += notes_user.username + ","
                    remaining_likes = estate.upvotes.all().count() - 2
                    msg = (
                        username_list
                        + " and "
                        + str(remaining_likes)
                        + " others upvoted your auction!"
                    )
                else:
                    if(estate.user != self.request.user ):
                        msg = q.user.username + " liked " + " your auction!"


            
            elif(q.estate and not q.bid):
                """auction notice"""
                is_auction_notice=True
                msg=q.estate.user.username+"posted an auction. "


            elif(q.bid and q.estate):
                """is_bid_notice"""

                is_bid_notice=True
                msg=q.other_user.username +" has put bid on your auction "+q.estate.title
            
            t=[q,is_like,is_auction_notice,is_bid_notice,msg,is_checked]
            res.append(t)
        return res

class BidHandleView(LoginRequiredMixin,View):
    def handle_silently(self):
        return JsonResponse({})
    def post(self, request, *args, **kwargs):
        intent=request.POST.get('intent')
        id_=request.POST.get('id')
        amount=request.POST.get('bid_amount')
        estate=get_object_or_404(Estate,id=id_)

        has_bid=True

        if(estate.user== request.user):
            return self.handle_silently();
        
        bid_html=None
        
        

        db_entry=Bids.objects.filter(estate=estate,user=request.user)
        if(intent== '0'):
            #add bid
            if(db_entry.exists()):
                print("already")
                self.handle_silently()
            else:
                db_entry=Bids.objects.create(estate=estate,user=request.user,bid_amount=amount)
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
            bid_list=get_bids_by_order(estate)
            bid_html=render_to_string('auctions/bid_list.html',context={'bids':bid_list},request=request)

        bid_form=BidForm(initial={'bid_amount':amount})
        context={
            "estate":estate,
            "has_bid":has_bid,
            "bid_form":bid_form,
            "user":estate.user,
        }
        
        html=render_to_string('auctions/bid_menu.html',context=context,request=request)

        return JsonResponse({'html':html,'bid_list':bid_html,})


        
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
            user=get_object_or_404(BidUser,id=note_id)
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




            


@login_required
def LikeAuction(request):
    auction = get_object_or_404(Estate, id=request.POST.get("id"))
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
        "estate": auction,
        "is_liked": is_liked,
        "is_disliked":is_disliked,
        
    }
   
    if is_ajax(request):
        like_html = render_to_string("auctions/f_like_section.html", context=context, request=request)
        dislike_html = render_to_string("auctions/f_dislike_section.html", context=context, request=request)
        
        json_data={
            "like_html": like_html,
            "dislike_html": dislike_html,

        }
        return JsonResponse(json_data)





def FavouriteAuction(request):
    estate = get_object_or_404(Estate, id=request.POST.get("id"))
    is_fav = False
    

    if estate.favourite.filter(id=request.user.id).exists():
        estate.favourite.remove(request.user)
    else:
        estate.favourite.add(request.user)
        is_fav = True
    context = {
        "estate": estate,
        "is_favourite": is_fav,
    }
    if is_ajax(request):
        html = render_to_string("auctions/f_fav_section.html", context, request=request)
        return JsonResponse({"form": html})

class FavouriteAuctionList(ListView):
    template_name="_index.html"
    context_object_name=INDEX_CONTEXT_NAME
    def get_queryset(self):
        favourite_posts = self.request.user.favourites.all()
        return get_auction_query_set(favourite_posts, self.request)
    
    
    



