from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.db import router, transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from user.models import User
from user.forms import UserCreationForm

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'nickname', 'email',)
    list_display_links = ('email',)
    list_filter = ('is_admin',)
    search_fields = ('nickname', 'email',)

    fieldsets = (
        ('info', {'fields': ('nickname', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('nickname', 'email', 'password',),
            },
        ),
    )

    filter_horizontal = ['followings', 'bookmark']
    ordering = ['id']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('nickname', 'email',)
        else:
            return ()
        
    add_form = UserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
    
    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url="", extra_context=None):        
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)