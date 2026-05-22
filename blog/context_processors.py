from .models import AccessRequest


def pending_access_requests(request):
    if not request.user.is_authenticated:
        return {'pending_requests_count': 0}
    count = AccessRequest.objects.filter(
        post__author=request.user,
        status=AccessRequest.STATUS_PENDING
    ).count()
    return {'pending_requests_count': count}
