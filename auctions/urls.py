from django.urls import path

from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('1234/', views.testy, name='xyz'),

    #auctions
    path('create/ads',views.AuctionCreate,name='create_auction'),
    path('edit/ads/<uuid:pk>',views.AuctionEdit,name='edit_auction'),
    path('delete/ads/<uuid:pk>',views.AuctionDeleteView.as_view(),name='delete_auction'),

    path('auction/<uuid:pk>',views.NewAuctionDetailView.as_view(),name='auction_detail'),
        
    
    #like
    path('like/auction/',views.LikeAuction,name='like_auction'),
    
    #favourite
    path('save/favourite/',views.FavouriteAuction,name='favourite_auction'),
    path('favourites/',views.FavouriteAuctionList.as_view(),name="favourite_lists"),



]