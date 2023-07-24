from rest_framework.permissions import BasePermission


class IsGhased(BasePermission):
    def has_permission(self, request, view):
        try:
            ghased = request.user.ghased
            setattr(request, 'ghased', ghased)
            return True
        except:
            return False
