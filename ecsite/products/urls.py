from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.Top.as_view(), name='top'),
    path('showResult/', views.ShowResult.as_view(), name='show_result'),
    # path('itemDetail/', views.ItemDetail.as_view(), name='item_detail'),
    # path('cart/', views.Cart.as_view(), name='cart'),
]
