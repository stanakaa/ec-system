from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path("registerUser/", views.RegisterUser.as_view(), name="register_user"),
    path("registerUserConfirm/", views.RegisterUserConfirm.as_view(), name="register_user_confirm"),
    path("registerUserCommit/", views.RegisterUserCommit.as_view(), name="register_user_commit"),

    path("userInfo/", views.UserInfo.as_view(), name="user_info"),
    path("updateUser/", views.UpdateUser.as_view(), name="update_user"),
    path("updateUserConfirm/", views.UpdateUserConfirm.as_view(), name="update_user_confirm"),
    path("updateUserCommit/", views.UpdateUserCommit.as_view(), name="update_user_commit"),
    path("withdrawConfirm/", views.WithdrawConfir.as_view(), name="withdraw_confirm")
]