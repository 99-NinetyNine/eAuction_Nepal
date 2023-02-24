from django.test import (
    TestCase,
    RequestFactory,
    AsyncRequestFactory,
)
import operator

from .models import (
    Auction,
    Bid,
    Notification,
)

from users.models import (
    User,
    Rating,
)

class HomePageTest(TestCase):
    def test_url_okay(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, '_index.html')

class RatingPriorityTest(TestCase):
    
    def setUp(self):
        self.user1=User.objects.create(username="user1")
        self.user2=User.objects.create(username="user2")
        self.user3=User.objects.create(username="user3")

        self.auction=Auction.objects.create(title="test auction",description="test desc",user=self.user1,price_min_value=2,price_max_value=40)
        self.auction.bids.create(user=self.user2,bid_amount=15)
        self.auction.bids.create(user=self.user3,bid_amount=5)
    
    #py manage.py test auctions.RatingPriorityTest
    def test_competition(self):
        Rating.objects.create(from_user=self.user1,to_user=self.user2,rating='4')
        Rating.objects.create(from_user=self.user3,to_user=self.user2,rating='3')
        Rating.objects.create(from_user=self.user1,to_user=self.user3,rating='1')
        from django.db.models import Avg

        qs=self.auction.bids.annotate(ratings=Avg('user__to__rating'))
        qs.order_by('bid_amount','-ratings')
        
        for k in qs:
            print("\namount",k.bid_amount)
            print("\nrating==\n",k.ratings)
