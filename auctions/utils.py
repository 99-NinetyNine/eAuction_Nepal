from .models import (
    Estate,
    Bids,
)

def get_auction_query_set(query_set,request,single_item=False):
    """
    returns a list of ["auction instance","is_liked","is_disliked","is_favourite"]
    """
    res=[]
    
    if(single_item):
        res.append(query_set)
        res.append(query_set.upvotes.filter(id=request.user.id).exists())
        res.append(query_set.downvotes.filter(id=request.user.id).exists())
        res.append(query_set.favourite.filter(id=request.user.id).exists())
        
        #note that i need list of lists haha..for unpacking
        res2=[]
        res2.append(res)
        return res2


    for q in query_set:
        t=[]
        t.append(q)
        t.append(q.upvotes.filter(id=request.user.id).exists())
        t.append(q.downvotes.filter(id=request.user.id).exists())
        t.append(q.favourite.filter(id=request.user.id).exists())
        res.append(t)
    
    return res

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_bids_by_order(estate):
    from django.db.models import Avg
    qs=estate.bids.annotate(ratings=Avg('user__to__rating')).order_by('bid_amount','-ratings')
    return qs
