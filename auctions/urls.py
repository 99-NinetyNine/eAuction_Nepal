from django.urls import path

from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    #auctions
    path('create/ads',views.AuctionCreate,name='create_auction'),
    path('edit/ads/<uuid:pk>',views.AuctionEdit,name='edit_auction'),
    path('delete/ads/<uuid:pk>',views.AuctionDeleteView.as_view(),name='delete_auction'),

    path('auction/<uuid:pk>',views.AuctionDetailView.as_view(),name='auction_detail'),
    path('auction/images/<uuid:pk>',views.ImageLinkView.as_view(),name='image_link'),

    
    #bids
    path('apply/bid/',views.BidCreateView.as_view(),name='apply_bid'),
    path('edit/bid/',views.BidUpdateView.as_view(),name='edit_bid'),
    path('delete/bid/',views.BidDeleteView.as_view(),name='delete_bid'),

    path('handle/bid/',views.BidHandleView.as_view(),name='handle_bid'),
    path('pending/bids/',views.BidPendingList.as_view(),name='bid_pending_lists'),
    
    #notification alerts
    path('alerts/',views.ListAlertsView.as_view(),name='notification_list'),
    path('alerts/handle',views.ListHandleView.as_view(),name='handle_notification'),
    
    #like
    path('like/auction/',views.LikeAuction,name='like_auction'),
    
    #favourite
    path('save/favourite/',views.FavouriteAuction,name='favourite_auction'),
    path('favourites/',views.FavouriteAuctionList.as_view(),name="favourite_lists"),



]