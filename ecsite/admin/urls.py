from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.adminLogin.as_view(), name="admin_login"),
    path("main/", views.adminMain.as_view(), name="admin_main"),
    path("logout/", views.adminLogout.as_view(), name="admin_logout"),

    path("itemList/", views.ItemList.as_view(), name="item_list"),
    path("itemRegister/", views.ItemRegister.as_view(), name="item_register"),
    path("itemUpdate/", views.ItemUpdate.as_view(), name="item_update"),
]