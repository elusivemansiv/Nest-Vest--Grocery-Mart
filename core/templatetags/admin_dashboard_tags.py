from django import template
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from core.models import CartOrder, Product, Category, Vendor
from userauths.models import User
import json
from datetime import datetime

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    underway_orders = CartOrder.objects.exclude(product_status='delivered').count()
    all_orders = CartOrder.objects.count()
    user_registrations = User.objects.count()
    all_products = Product.objects.count()

    # Revenue
    rev_aggregate = CartOrder.objects.aggregate(total=Sum('price'))
    total_revenue = rev_aggregate['total'] if rev_aggregate['total'] is not None else 0

    # Order Status breakdowns
    delivered_orders = CartOrder.objects.filter(product_status='delivered').count()
    processing_orders = CartOrder.objects.filter(product_status='processing').count()
    shipped_orders = CartOrder.objects.filter(product_status='shipped').count()

    # Store catalogs
    total_categories = Category.objects.count()
    total_vendors = Vendor.objects.count()

    # Recent items
    recent_orders = CartOrder.objects.select_related('user').order_by('-id')[:6]
    recent_products = Product.objects.select_related('category', 'vendor').order_by('-id')[:5]

    # Chart data: Sales and Products grouped by month
    sales_data = CartOrder.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(count=Count('id')).order_by('month')
    products_data = Product.objects.annotate(month=TruncMonth('date')).values('month').annotate(count=Count('id')).order_by('month')
    
    # Process into lists for chart
    labels = set()
    for s in sales_data:
        if s['month']:
            labels.add(s['month'].strftime("%b %Y"))
    for p in products_data:
        if p['month']:
            labels.add(p['month'].strftime("%b %Y"))
            
    # Sort labels by date
    try:
        labels_list = sorted(list(labels), key=lambda d: datetime.strptime(d, "%b %Y"))
    except Exception:
        labels_list = sorted(list(labels))
    
    sales_counts = []
    product_counts = []
    
    for label in labels_list:
        s_count = 0
        for s in sales_data:
            if s['month'] and s['month'].strftime("%b %Y") == label:
                s_count = s['count']
                break
        sales_counts.append(s_count)
        
        p_count = 0
        for p in products_data:
            if p['month'] and p['month'].strftime("%b %Y") == label:
                p_count = p['count']
                break
        product_counts.append(p_count)

    return {
        'underway_orders': underway_orders,
        'all_orders': all_orders,
        'user_registrations': user_registrations,
        'all_products': all_products,
        'total_revenue': total_revenue,
        'delivered_orders': delivered_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'total_categories': total_categories,
        'total_vendors': total_vendors,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
        'chart_labels': json.dumps(labels_list),
        'chart_sales': json.dumps(sales_counts),
        'chart_products': json.dumps(product_counts),
    }


@register.simple_tag
def get_site_settings():
    from site_settings.models import SiteSettings
    try:
        return SiteSettings.objects.first()
    except Exception:
        return None


