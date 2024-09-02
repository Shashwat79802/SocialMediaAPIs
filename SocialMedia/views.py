from django.db import IntegrityError
from django.db.models import ForeignKey
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserFriendsSerializer
from .models import UserFriends
from .pagination import CustomPagination
from .throttling import FriendRequestThrottle

User = get_user_model()


class UserSeachView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['full_name', 'email']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class UserFriendsViewCreate(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    @staticmethod
    def friend_request_pending_conditions(friendship_instance, request_type):
        if request_type == 'accept-friend-request':
            friendship_instance.status = 'accepted'
            friendship_instance.save()
            return Response({"detail": "Friend request accepted."}, status=200)
        elif request_type == 'reject-friend-request':
            friendship_instance.status = 'rejected'
            friendship_instance.save()
            return Response({"detail": "Friend request rejected."}, status=200)
        elif request_type == 'send-friend-request':
            return Response({"detail": "Friend request already sent."}, status=400)

    @staticmethod
    def friend_request_accepted_conditions(friendship_instance, request_type):
        if request_type == 'accept-friend-request':
            return Response({"detail": "Already friends."}, status=400)
        elif request_type == 'send-friend-request':
            return Response({"detail": "Already friends."}, status=400)
        elif request_type == 'reject-friend-request':
            friendship_instance.delete()
            return Response({"detail": "Friend removed."}, status=200)

    @staticmethod
    def friend_request_rejected_conditions(friendship_instance, request_type):
        if request_type == 'send-friend-request':
            friendship_instance.status = 'pending'
            friendship_instance.save()
            return Response({"detail": "Friend request sent."}, status=200)
        elif request_type == 'reject-friend-request':
            return Response({"detail": "Friend request already rejected."}, status=400)
        elif request_type == 'accept-friend-request':
            return Response({"detail": "Friend request already rejected."}, status=400)

    @staticmethod
    def get(request):
        if request.resolver_match.url_name == 'get-friends':
            status = 'accepted'
        elif request.resolver_match.url_name == 'received-friend-requests':
            status = 'pending'
        else:
            return Response({"detail": "Invalid request."}, status=400)

        friends = UserFriends.objects.filter(user=request.user, status=status)

        if not friends:
            return Response({"detail": "No friends found."}, status=200)

        serializer = UserFriendsSerializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request, friend_id):
        try:
            friend_request_exists = UserFriends.objects.filter(user=request.user, friend_id=friend_id).first()
        except IntegrityError:
            return Response({"detail": "Incorrect User ID"}, status=400)
        if friend_request_exists:
            if friend_request_exists.status == 'pending':
                return self.friend_request_pending_conditions(friend_request_exists, request.resolver_match.url_name)
            elif friend_request_exists.status == 'accepted':
                return self.friend_request_accepted_conditions(friend_request_exists, request.resolver_match.url_name)
            elif friend_request_exists.status == 'rejected':
                return self.friend_request_rejected_conditions(friend_request_exists, request.resolver_match.url_name)
        else:
            try:
                UserFriends.objects.create(friend=request.user, user_id=friend_id, status='pending')
            except IntegrityError:
                return Response({"detail": "Incorrect User ID"}, status=400)
            return Response({"detail": "Friend request sent."}, status=200)
