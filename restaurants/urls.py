from django.urls import path
from .views import GetRestaurants,MenuApiView,OrderListView,GetTags, GetSocial, GetCart, ShareReview

urlpatterns = [
    path('qeats/v1/restaurants', GetRestaurants.as_view()),
    path('qeats/v1/menu', MenuApiView.as_view()),
    path('qeats/v1/orders/', OrderListView.as_view()),
    path('qeats/v1/tags', GetTags.as_view()),
    path('qeats/v1/social', GetSocial.as_view()),
    path('qeats/v1/cart', GetCart.as_view()),
    path('qeats/v1/review/share', ShareReview.as_view())
]
