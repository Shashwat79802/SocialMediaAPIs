from django.urls import path
from .views import *


urlpatterns = [
    path('search-users/', UserSeachView.as_view(), name='search-users'),
    path('friends/', UserFriendsViewCreate.as_view(), name='get-friends'),
    path('friend-requests/', UserFriendsViewCreate.as_view(), name='received-friend-requests'),
    path('make-friend/<int:friend_id>/', UserFriendsViewCreate.as_view(), name='send-friend-request'),
    path('reject-friend/<int:friend_id>/', UserFriendsViewCreate.as_view(), name='reject-friend-request'),
    path('accept-friend/<int:friend_id>/', UserFriendsViewCreate.as_view(), name='accept-friend-request'),
]
