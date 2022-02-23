from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from api.authentication.forms import UserChangeForm, UserCreationForm
from api.authentication.models import Code, User


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Meta", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    readonly_fields = ("date_joined",)
    search_fields = ("email", "full_name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
