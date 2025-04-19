from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsAssociation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'association_staff'
    
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'
    
class IsCenterStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'center_staff'
    
class IsCenterStaffForMaterial(permissions.BasePermission):
    """
    Custom permission to only allow center staff to manage materials in their center.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and is center staff
        if not request.user.is_authenticated or request.user.role != 'center_staff':
            return False
        
        # For POST requests, check if the center matches the user's center
        if request.method == 'POST':
            center_id = request.data.get('center')
            return str(request.user.userprofile.center.id) == str(center_id)
        
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the material belongs to the user's center
        return obj.center == request.user.userprofile.center
    
    