from core.models import Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from django.db.models import Min, Max
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            wishlist = wishlist_model.objects.filter(user=request.user).count()
        except Exception:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
            
        try:
            address = Address.objects.filter(user=request.user).first()
        except Exception:
            address = None
    else:
        wishlist = 0
        address = None

    from site_settings.models import SiteSettings, ContactInfo, SocialLink, SupportNumber, CallToAction
    try:
        site_settings = SiteSettings.objects.first()
    except Exception:
        site_settings = None

    try:
        contact_info = ContactInfo.objects.first()
    except Exception:
        contact_info = None

    try:
        social_links = SocialLink.objects.first()
    except Exception:
        social_links = None
    support_numbers = SupportNumber.objects.all()
    
    try:
        cta = CallToAction.objects.first()
    except Exception:
        cta = None
    
    from site_settings.models import FooterLinkColumn
    footer_columns = FooterLinkColumn.objects.prefetch_related('links').all()

    return {
        'categories':categories,
        'wishlist':wishlist,
        'address':address,
        'vendors':vendors,
        'min_max_price':min_max_price,
        'site_settings_data': site_settings,
        'contact_info_data': contact_info,
        'social_links': social_links,
        'support_numbers': support_numbers,
        'cta': cta,
    }