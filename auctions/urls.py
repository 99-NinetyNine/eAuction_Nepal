from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),

    #auctions
    path('create/ads',views.AuctionCreateView.as_view(),name='create_auction'),
    path('edit/ads/<uuid:pk>',views.AuctionEditView.as_view(),name='edit_auction'),
    path('delete/ads/<uuid:pk>',views.AuctionDeleteView.as_view(),name='delete_auction'),

    path('auction/<uuid:pk>',views.EstateDetailView.as_view(),name='auction_detail'),
    path('auction/images/<uuid:pk>',views.ImageLinkView.as_view(),name='image_link'),

    
    #bids
    path('apply/bid/<uuid:pk>',views.BidCreateView.as_view(),name='apply_bid'),
    path('edit/bid/<uuid:pk>',views.BidUpdateView.as_view(),name='edit_bid'),
    path('delete/bid/<uuid:pk>',views.BidDeleteView.as_view(),name='delete_bid'),

    path('bid/detail/<uuid:pk>',views.BidDetailView.as_view(),name='bid_detail'),
    
    #notification alerts
    path('alerts/',view.ListAlertsView.as_view(),name='notification_list'),
    path('alert/<uuid:pk>',views.NotificationDetailView.as_view(),name='notification_detail'),




]