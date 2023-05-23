from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    path('email/', views.SendEmailView.as_view(), name='send_email'),
    path('verify/', views.VerificationEmailView.as_view(), name='verify_email'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #follow 기능 url
    path("<int:user_id>/follow/", views.FollowView.as_view(), name="follow_user"),
    path("<int:user_id>/followings/", views.FollowingView.as_view(), name="followings"),
    path("<int:user_id>/followers/", views.FollowerView.as_view(), name="followers"),

    #bookmark 기능 url
    path("<int:user_id>/bookmark/", views.BookMarkView.as_view(), name="bookmark_view"),
    path("<int:user_id>/bookmark_list/",views.BookMarkListView.as_view(),name="bookmark_list_view",),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]