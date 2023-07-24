from rest_framework.request import Request

from accounts._ports.permissions import IsGhasedInterface


class IsGhased(IsGhasedInterface):
    def has_permission(self, request: Request, view):
        try:
            ghased = request.user.ghased
            setattr(request, 'ghased', ghased)
            return request
        except:
            return False
