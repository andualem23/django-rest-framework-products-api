from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    