from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth
from core.models import CartOrder, Product
from userauths.models import User
import json

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    underway_orders = CartOrder.objects.exclude(product_status='delivered').count()
    all_orders = CartOrder.objects.count()
    user_registrations = User.objects.count()
    all_products = Product.objects.count()

    # Chart data: Sales and Products grouped by month (last 12 months roughly, or all for simplicity)
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
    from datetime import datetime
    labels_list = sorted(list(labels), key=lambda d: datetime.strptime(d, "%b %Y"))
    
    sales_counts = []
    product_counts = []
    
    for label in labels_list:
        # Find sales for this month
        s_count = 0
        for s in sales_data:
            if s['month'] and s['month'].strftime("%b %Y") == label:
                s_count = s['count']
                break
        sales_counts.append(s_count)
        
        # Find products for this month
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
        'chart_labels': json.dumps(labels_list),
        'chart_sales': json.dumps(sales_counts),
        'chart_products': json.dumps(product_counts),
    }
