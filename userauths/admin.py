from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from userauths.models import User, ContactUs, Profile


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username")


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['email', 'username', 'bio', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['email', 'username']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'bio')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.password and not (obj.password.startswith('pbkdf2_') or obj.password.startswith('argon2') or obj.password.startswith('bcrypt_')):
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'bio', 'phone', 'verified']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile, ProfileAdmin)