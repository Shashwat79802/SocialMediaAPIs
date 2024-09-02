from rest_framework.throttling import UserRateThrottle
from datetime import timedelta
from django.utils import timezone

from SocialMedia.models import UserFriends


class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'

    def allow_request(self, request, view):
        if request.method != 'POST' or request.resolver_match.url_name != 'send-friend-request':
            return True

        user = request.user
        now = timezone.now()
        one_minute_ago = now - timedelta(minutes=1)

        recent_requests_count = UserFriends.objects.filter(
            user=user,
            status='pending',
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return False

        return super().allow_request(request, view)
