from django.db import models

class SiteSettings(models.Model):
    title = models.CharField(max_length=200, default="My Site")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    footer_logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    favicon = models.ImageField(upload_to="settings/", blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    footer_description = models.TextField(blank=True, null=True)
    developer_company = models.CharField(max_length=255, blank=True, null=True)
    developer_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.title

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ContactInfo(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    working_hours = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return "Contact Information"


class HomePageTheme(models.Model):
    name = models.CharField(max_length=100, default="Default Theme")
    primary_color = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. #ff0000")
    
    class Meta:
        verbose_name = "Home Pages Theme"
        verbose_name_plural = "Home Pages Theme"

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    facebook_url = models.URLField(blank=True, null=True, help_text="Leave blank to hide Facebook icon")
    twitter_url = models.URLField(blank=True, null=True, help_text="Leave blank to hide Twitter icon")
    instagram_url = models.URLField(blank=True, null=True, help_text="Leave blank to hide Instagram icon")
    pinterest_url = models.URLField(blank=True, null=True, help_text="Leave blank to hide Pinterest icon")
    youtube_url = models.URLField(blank=True, null=True, help_text="Leave blank to hide YouTube icon")

    class Meta:
        verbose_name = "Socail links" # Purposely misspelled as in screenshot
        verbose_name_plural = "Socail links"

    def __str__(self):
        return "Social Links"


class SupportNumber(models.Model):
    label = models.CharField(max_length=100, help_text="e.g. Sales, Support", blank=True, null=True)
    phone = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Support Numbers"
        verbose_name_plural = "Support Numbers"

    def __str__(self):
        if self.label:
            return f"{self.label}: {self.phone}"
        return self.phone

class FooterLinkColumn(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Footer Link Column"
        verbose_name_plural = "Footer Link Columns"
        ordering = ['order']

    def __str__(self):
        return self.title

class FooterLink(models.Model):
    column = models.ForeignKey(FooterLinkColumn, related_name='links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, default="#")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"
        ordering = ['order']

    def __str__(self):
        return self.name

class Slider(models.Model):
    image = models.ImageField(upload_to="slider/", blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    sub_heading = models.CharField(max_length=255, blank=True, null=True)
    link_text = models.CharField(max_length=50, default="Shop Now", blank=True, null=True)
    link_url = models.CharField(max_length=255, default="#", blank=True, null=True)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
        return self.heading or "Slider"

class HomeBanner(models.Model):
    image = models.ImageField(upload_to="banner/", blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    link_text = models.CharField(max_length=50, default="Shop Now", blank=True, null=True)
    link_url = models.CharField(max_length=255, default="#", blank=True, null=True)

    class Meta:
        verbose_name = "Home Banner"
        verbose_name_plural = "Home Banners"

    def __str__(self):
        return self.heading or "Home Banner"

class CallToAction(models.Model):
    image = models.ImageField(upload_to="cta/", blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    sub_heading = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Call To Action"
        verbose_name_plural = "Call To Action"

    def __str__(self):
        return self.heading or "Call To Action"
