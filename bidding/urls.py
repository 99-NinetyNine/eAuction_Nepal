from django.urls import path

from . import views
urlpatterns = [
 #bids
    path('pay/initial/money/',views.pay_initial_view,name="pay_initial"),
    path('pay/final/money/',views.pay_final_view,name="pay_last"),
    
    
    path('apply/bid/',views.BidCreateView.as_view(),name='apply_bid'),
    path('edit/bid/',views.BidUpdateView.as_view(),name='edit_bid'),
    path('delete/bid/',views.BidDeleteView.as_view(),name='delete_bid'),

    path('handle/bid/',views.BidHandleView.as_view(),name='handle_bid'),
    path('pending/bids/',views.BidPendingList.as_view(),name='bid_pending_lists'),
    
    
]