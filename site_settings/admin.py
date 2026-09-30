from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings,
    ContactInfo,
    HomePageTheme,
    SocialLink,
    SupportNumber,
    FooterLinkColumn,
    FooterLink,
    Slider,
    HomeBanner,
    CallToAction,
)


class NoLogModelAdmin(admin.ModelAdmin):
    def log_addition(self, *args, **kwargs):
        pass

    def log_change(self, *args, **kwargs):
        pass

    def log_deletion(self, *args, **kwargs):
        pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(NoLogModelAdmin):
    list_display = ['title', 'logo_preview', 'copyright', 'developer_company']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 32px; max-width: 100px; object-fit: contain;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo"


@admin.register(ContactInfo)
class ContactInfoAdmin(NoLogModelAdmin):
    list_display = ['email', 'phone', 'working_hours', 'address']


@admin.register(HomePageTheme)
class HomePageThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_badge']

    def color_badge(self, obj):
        if obj.primary_color:
            return format_html('<span style="display: inline-flex; align-items: center; gap: 6px;"><span style="width: 16px; height: 16px; border-radius: 4px; background-color: {}; display: inline-block; border: 1px solid #cbd5e1;"></span> <code>{}</code></span>', obj.primary_color, obj.primary_color)
        return "-"
    color_badge.short_description = "Primary Color"


@admin.register(SocialLink)
class SocialLinkAdmin(NoLogModelAdmin):
    list_display = ['__str__', 'active_networks']

    def active_networks(self, obj):
        networks = []
        if obj.facebook_url: networks.append('Facebook')
        if obj.twitter_url: networks.append('Twitter')
        if obj.instagram_url: networks.append('Instagram')
        if obj.pinterest_url: networks.append('Pinterest')
        if obj.youtube_url: networks.append('YouTube')
        return ", ".join(networks) if networks else "None configured"
    active_networks.short_description = "Active Links"


@admin.register(SupportNumber)
class SupportNumberAdmin(NoLogModelAdmin):
    list_display = ['phone', 'label']


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1


@admin.register(FooterLinkColumn)
class FooterLinkColumnAdmin(NoLogModelAdmin):
    list_display = ['title', 'order', 'links_count']
    inlines = [FooterLinkInline]

    def links_count(self, obj):
        return obj.links.count()
    links_count.short_description = "Total Links"


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['slider_image_preview', 'heading', 'sub_heading', 'link_text', 'link_url']

    def slider_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 35px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return "-"
    slider_image_preview.short_description = "Slide Image"


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['banner_image_preview', 'heading', 'link_text', 'link_url']

    def banner_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 35px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return "-"
    banner_image_preview.short_description = "Banner Image"


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ['cta_image_preview', 'heading', 'sub_heading']

    def cta_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 35px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return "-"
    cta_image_preview.short_description = "CTA Image"
