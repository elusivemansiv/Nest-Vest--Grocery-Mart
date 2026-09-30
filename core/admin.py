from django.contrib import admin
from django.utils.html import format_html
from core.models import CartOrderProducts, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        'product_image_preview',
        'title',
        'price',
        'category',
        'vendor',
        'product_status',
        'featured',
        'deal_of_the_day',
        'is_top_selling',
        'is_trending',
        'is_top_rated',
        'date',
    ]
    list_display_links = ['title']
    list_editable = [
        'price',
        'product_status',
        'featured',
        'deal_of_the_day',
        'is_top_selling',
        'is_trending',
        'is_top_rated',
    ]
    search_fields = ['title', 'sku', 'pid']
    list_filter = [
        'category',
        'vendor',
        'product_status',
        'featured',
        'deal_of_the_day',
        'is_top_selling',
        'is_trending',
        'is_top_rated',
        'date',
    ]
    list_per_page = 20
    date_hierarchy = 'date'

    fieldsets = (
        ("Basic Information", {
            'fields': ('title', 'image', 'user', 'category', 'vendor', 'type'),
        }),
        ("Pricing & Stock", {
            'fields': ('price', 'old_price', 'stock_count', 'in_stock', 'life', 'mfd'),
        }),
        ("Product Description & Specs", {
            'fields': ('description', 'specifications', 'tags'),
            'classes': ('collapse',),
        }),
        ("Status & Badges", {
            'fields': (
                'product_status',
                'status',
                'featured',
                'digital',
                'deal_of_the_day',
                'deal_end_date',
                'is_top_selling',
                'is_trending',
                'is_top_rated',
            ),
        }),
    )

    def product_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.08);" />', obj.image.url)
        return "-"
    product_image_preview.short_description = "Image"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_image_preview', 'title', 'product_count_badge']
    search_fields = ['title']
    list_per_page = 20

    def category_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.08);" />', obj.image.url)
        return "-"
    category_image_preview.short_description = "Image"

    def product_count_badge(self, obj):
        count = obj.product_count()
        return format_html('<span class="badge badge-info" style="font-weight: 600;">{} Products</span>', count)
    product_count_badge.short_description = "Products In Category"


class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_image_preview', 'title', 'user', 'contact', 'date']
    search_fields = ['title', 'contact', 'user__username', 'user__email']
    list_filter = ['date']
    list_per_page = 20

    def vendor_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.08);" />', obj.image.url)
        return "-"
    vendor_image_preview.short_description = "Logo"


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['sku_badge', 'user', 'price_formatted', 'paid_status_badge', 'product_status', 'order_date']
    list_editable = ['product_status']
    list_filter = ['paid_status', 'product_status', 'order_date']
    search_fields = ['sku', 'user__username', 'user__email']
    date_hierarchy = 'order_date'
    list_per_page = 25

    def sku_badge(self, obj):
        return format_html('<strong class="text-success">#{}</strong>', obj.sku)
    sku_badge.short_description = "Order SKU"

    def price_formatted(self, obj):
        return format_html('<strong>${}</strong>', obj.price)
    price_formatted.short_description = "Total Amount"

    def paid_status_badge(self, obj):
        if obj.paid_status:
            return format_html('<span class="badge badge-success">Paid</span>')
        return format_html('<span class="badge badge-danger">Unpaid</span>')
    paid_status_badge.short_description = "Payment Status"


class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'vendor', 'product', 'qty', 'price', 'total']
    list_filter = ['vendor', 'product_status']
    search_fields = ['order__sku', 'invoice_no', 'item']
    list_per_page = 25


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating_stars', 'review_snippet', 'date']
    list_filter = ['rating', 'date']
    search_fields = ['user__username', 'product__title', 'review']
    list_per_page = 25

    def rating_stars(self, obj):
        stars = '★' * (obj.rating or 0)
        return format_html('<span style="color: #f59e0b; font-size: 1.1rem; letter-spacing: 2px;">{}</span>', stars)
    rating_stars.short_description = "Rating"

    def review_snippet(self, obj):
        if len(obj.review) > 60:
            return obj.review[:60] + "..."
        return obj.review
    review_snippet.short_description = "Review"


class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    search_fields = ['user__username', 'product__title']
    list_filter = ['date']
    list_per_page = 25


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
    list_editable = ['status']
    search_fields = ['user__username', 'address']
    list_filter = ['status']
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(wishlist_model, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
