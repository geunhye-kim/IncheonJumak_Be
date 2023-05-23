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
        ('info', {'fields': ('nickname', 'email', 'password', 'following',)}),
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

    exclude = ['username']
    filter_horizontal = ['following']
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
        
    # def _add_view(self, request, form_url="", extra_context=None):
    #     # It's an error for a user to have add permission but NOT change
    #     # permission for users. If we allowed such users to add users, they
    #     # could create superusers, which would mean they would essentially have
    #     # the permission to change users. To avoid the problem entirely, we
    #     # disallow users from adding users if they don't have change
    #     # permission.
    #     if not self.has_change_permission(request):
    #         print("1111111111")
    #         if self.has_add_permission(request) and settings.DEBUG:
    #             print("222222222")
    #             # Raise Http404 in debug mode so that the user gets a helpful
    #             # error message.
    #             raise Http404(
    #                 'Your user does not have the "Change user" permission. In '
    #                 "order to add users, Django requires that your user "
    #                 'account have both the "Add user" and "Change user" '
    #                 "permissions set."
    #             )
    #         raise PermissionDenied
    #     if extra_context is None:
    #         print("33333333")
    #         extra_context = {}
    #     nickname_field = self.opts.get_field(self.model.USERNAME_FIELD)
    #     defaults = {
    #         "auto_populated_fields": (),
    #         "username_help_text": nickname_field.help_text,
    #     }
    #     extra_context.update(defaults)
    #     print("444444")
    #     return super().add_view(request, form_url, extra_context)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)