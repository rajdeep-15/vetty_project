from django.urls import path
from crypto.views import CoinListView,CoinCategoryView,CoinDataView

urlpatterns = [
    path('coinlist/', CoinListView.as_view(), name='coins-list'),
    path('coincategory/', CoinCategoryView.as_view(), name='coins-by-category'),
    path('coin_market_data/', CoinDataView.as_view(), name='coins-market-data'),
]