from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import BasePermission


class AllowSignupAndLogin(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, 'action') and hasattr(view, 'basename'):
            if view.action in ['create'] and view.basename in ['user', 'token']:
                return True
        elif request.method == 'POST' and view.__class__.__name__ == 'CustomTokenCreateView':
            return True
        return request.user.is_authenticated

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete.
    Read permissions are allowed to any request.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff



class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the snippet or an admin.
        return request.user and (request.user.is_staff or obj.user == request.user)
