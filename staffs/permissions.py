from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q

from staffs.models import StaffDesignation, Staff

User = get_user_model()

class StaffPermissionBackend(BaseBackend):

    def to_set(self, perms):
        perms = perms.values_list('content_type__app_label', 'codename')
        return {"%s.%s" % (ct, name) for ct, name in perms}

    def get_user_permissions(self, user_obj, obj=None):
        return self.to_set(user_obj.staff.permissions.all())

    def get_group_permissions(self, user_obj, obj=None):
        return self.to_set(user_obj.staff.designation.permissions.all())


def get_available_permissions():
    permission_instances = {}
    for permission in Permission.objects.filter(~Q(content_type__app_label__in=[
        'auth', 'admin', 'mailqueue', 'registration', 'contenttypes', 'users', 'sessions'
    ])).order_by('content_type__app_label'):

        KEY = permission.content_type.app_label
        if KEY not in permission_instances:
            permission_instances[KEY] = [permission]
        else:
            permission_instances[KEY].append(permission)

    return permission_instances


def get_allowed_permissions(instance):
    if isinstance(instance, StaffDesignation):
        return instance.permissions.all().values_list('id', flat=True)
    elif isinstance(instance, Staff):
        return {
            *list(instance.designation.permissions.all().values_list('id', flat=True)),
            *list(instance.permissions.all().values_list('id', flat=True))
        }
    else:
        raise TypeError('Invalid instance object.')
    
    
