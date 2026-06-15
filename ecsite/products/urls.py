from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.Top.as_view(), name='top'),
    path('showResult/', views.ShowResult.as_view(), name='show_result'),
    path('itemDetail/<int:item_id>', views.ItemDetail.as_view(), name='item_detail'),

    path('addCart/<int:item_id>', views.AddCart.as_view(), name='add_cart'),
    path('cart/', views.ShowCart.as_view(), name="cart"),
    path('deleteCart/<int:cart_id>', views.DeleteCart.as_view(), name="delete_cart"),
    path('updateCart/<int:cart_id>', views.UpdateCart.as_view(), name='update_cart'),
]
