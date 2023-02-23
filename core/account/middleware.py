from django.utils.deprecation import MiddlewareMixin
from account.models import Profile


class AddProfileToRequest(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'profile') and request.user.is_authenticated:
            request.profile = Profile.objects.get(user=request.user)

