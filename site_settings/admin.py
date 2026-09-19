from django.contrib import admin
from .models import SiteSettings, ContactInfo, HomePageTheme, SocialLink, SupportNumber, FooterLinkColumn, FooterLink, Slider, HomeBanner, CallToAction

class NoLogModelAdmin(admin.ModelAdmin):
    def log_addition(self, *args, **kwargs):
        pass
    def log_change(self, *args, **kwargs):
        pass
    def log_deletion(self, *args, **kwargs):
        pass

@admin.register(SiteSettings)
class SiteSettingsAdmin(NoLogModelAdmin):
    pass

@admin.register(ContactInfo)
class ContactInfoAdmin(NoLogModelAdmin):
    pass

@admin.register(HomePageTheme)
class HomePageThemeAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialLink)
class SocialLinkAdmin(NoLogModelAdmin):
    pass

@admin.register(SupportNumber)
class SupportNumberAdmin(NoLogModelAdmin):
    list_display = ['phone', 'label']

class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1

@admin.register(FooterLinkColumn)
class FooterLinkColumnAdmin(NoLogModelAdmin):
    list_display = ['title', 'order']
    inlines = [FooterLinkInline]

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    pass

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    pass

@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    pass
