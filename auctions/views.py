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


from bidding.forms import BidForm
from .forms import (
    AuctionForm,
)

INDEX_CONTEXT_NAME="auctions"

        


class HomeView(LoginRequiredMixin,ListView):
    model=Auction
    template_name='_index.html'
    context_object_name=INDEX_CONTEXT_NAME

    def get_queryset(self,**kwargs):
        return Auction.query.get_serialized_query_set(Auction.objects.all(),self.request)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context
        
    

def AuctionCreate(request):
    
    ImageFormset = modelformset_factory(
        AuctionImage, fields=("about", "photo",),
    )
    if request.method == "POST":
        form = AuctionForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES)
        if form.is_valid() and formset.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()
            no_of_formset = 0
            no_of_error = 0
            for f in formset:
                try:
                    auction_image = AuctionImage(
                        auction=auction,
                        about=f.cleaned_data.get("about"),
                        photo=f.cleaned_data.get("photo"),
                    )
                    
                    auction_image.save()
                    
                except Exception as e:
                    print("error @ formset",e)
                    if not auction_image:
                        no_of_error += 1

                no_of_formset += 1
            
            if no_of_formset == no_of_error:
                auction.delete()
                messages.success(request, "Post has not created.")
                return redirect("create_auction")

            messages.success(request, "Post has been successfully created.")
            return redirect("home")

    else:
        form=AuctionForm()
        formset = ImageFormset(queryset=AuctionImage.objects.none())
    return render(request, "auction/form/create.html", {"form":form, "formset": formset,})

def AuctionEdit(request, pk):
    auction = get_object_or_404(Auction, id=pk)
    if auction.user != request.user:
        raise Http404()
    ImageFormset = modelformset_factory(
        AuctionImage, fields=("about", "photo",), extra=4, max_num=4
    )
    if request.method == "POST":
        form = AuctionForm(request.POST or None, instance=auction)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            data = AuctionImage.objects.filter(auction=auction)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data["id"] is None:
                        photo = AuctionImage(
                            auction=auction, photo=f.cleaned_data.get("photo")
                        )
                        photo.save()
                    elif f.cleaned_data["photo"] is False:
                        photo = AuctionImage.objects.get(
                            id=request.POST.get("form-" + str(index) + "-id")
                        )
                        photo.delete()
                    else:
                        photo = AuctionImage(
                            auction=auction, photo=f.cleaned_data.get("photo")
                        )
                        d = AuctionImage.objects.get(id=data[index].id)
                        d.image = photo.photo
                        d.save()
            messages.success(request, "Post has been successfully updated!")
            return HttpResponseRedirect(auction.get_absolute_url())
    else:
        form = AuctionForm(instance=auction)
        formset = ImageFormset(queryset=AuctionImage.objects.filter(auction=auction))
    context = {
        "form": form,
        "auction": auction,
        "formset": formset,
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
        print(self.pk)
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

        has_bid,form=self.get_bid_form()
        context["has_bid"]=has_bid
        context["bid_form"]=form
        

        return context
    
    
    

    
class ImageLinkView(DetailView):

    model=AuctionImage
    template_name='auction/detail/image.html'


        
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