from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from userauths.models import User, ContactUs, Profile


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username")


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = [ProfileInline]
    list_display = ['email', 'username', 'staff_badge', 'superuser_badge', 'active_badge', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    list_per_page = 25

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

    def staff_badge(self, obj):
        if obj.is_staff:
            return format_html('<span class="badge badge-success">Staff</span>')
        return format_html('<span class="badge badge-secondary">Member</span>')
    staff_badge.short_description = "Staff Status"

    def superuser_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span class="badge badge-primary">Superuser</span>')
        return "-"
    superuser_badge.short_description = "Admin"

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success"><i class="fas fa-check"></i> Active</span>')
        return format_html('<span class="badge badge-danger">Disabled</span>')
    active_badge.short_description = "Account Status"

    def save_model(self, request, obj, form, change):
        if obj.password and not (obj.password.startswith('pbkdf2_') or obj.password.startswith('argon2') or obj.password.startswith('bcrypt_')):
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'subject', 'message_snippet']
    search_fields = ['full_name', 'email', 'subject', 'phone']
    list_per_page = 25

    def message_snippet(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + "..."
        return obj.message
    message_snippet.short_description = "Message"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_image_preview', 'user', 'full_name', 'phone', 'verified_badge']
    list_filter = ['verified']
    search_fields = ['user__email', 'user__username', 'full_name', 'phone']
    list_per_page = 25

    def profile_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.08);" />', obj.image.url)
        return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: #f1f5f9; display: flex; align-items: center; justify-content: center; color: #94a3b8;"><i class="fas fa-user"></i></div>')
    profile_image_preview.short_description = "Avatar"

    def verified_badge(self, obj):
        if obj.verified:
            return format_html('<span class="badge badge-success"><i class="fas fa-check-circle"></i> Verified</span>')
        return format_html('<span class="badge badge-warning">Unverified</span>')
    verified_badge.short_description = "Verification"


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile, ProfileAdmin)