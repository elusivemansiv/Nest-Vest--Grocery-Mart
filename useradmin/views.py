import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from core.models import CartOrder, CartOrderProducts, Product, Category, Vendor, Address
from django.db.models import Sum, Q
from userauths.models import User
from useradmin.forms import AddProductForm, VendorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST


def get_user_vendor(user):
    return Vendor.objects.filter(user=user).first()


@login_required
@staff_member_required
def dashboard(request):
    this_month = datetime.datetime.now().month

    if request.user.is_superuser:
        revenue = CartOrder.objects.aggregate(price=Sum("price"))
        if revenue['price'] is None:
            revenue['price'] = 0
        total_orders_count = CartOrder.objects.count()
        all_products = Product.objects.all()
        all_categories = Category.objects.all()
        new_customers = User.objects.all().order_by("-id")[:6]
        latest_orders = list(CartOrder.objects.all().order_by("-id")[:10])
        for ord_obj in latest_orders:
            ord_obj.vendor_total = ord_obj.price

        m_rev = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))
        monthly_revenue = m_rev if m_rev['price'] is not None else {'price': 0}
    else:
        vendor = get_user_vendor(request.user)
        if not vendor:
            revenue = {'price': 0}
            monthly_revenue = {'price': 0}
            total_orders_count = 0
            all_products = Product.objects.filter(user=request.user)
            all_categories = Category.objects.all()
            new_customers = User.objects.none()
            latest_orders = []
        else:
            vendor_items = CartOrderProducts.objects.filter(
                Q(vendor=vendor) | Q(product__user=request.user)
            )
            vendor_orders = CartOrder.objects.filter(
                cartorderproducts__in=vendor_items
            ).distinct().order_by("-id")

            rev_val = vendor_items.aggregate(price=Sum("total"))
            revenue = rev_val if rev_val['price'] is not None else {'price': 0}

            m_val = vendor_items.filter(order__order_date__month=this_month).aggregate(price=Sum("total"))
            monthly_revenue = m_val if m_val['price'] is not None else {'price': 0}

            total_orders_count = vendor_orders.count()
            all_products = Product.objects.filter(Q(vendor=vendor) | Q(user=request.user))
            all_categories = Category.objects.all()
            new_customers = User.objects.filter(cartorder__in=vendor_orders).distinct().order_by("-id")[:6]

            latest_orders = list(vendor_orders[:10])
            for ord_obj in latest_orders:
                ord_vendor_items = vendor_items.filter(order=ord_obj)
                ord_total = ord_vendor_items.aggregate(s=Sum('total'))['s'] or 0
                ord_obj.vendor_total = ord_total

    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
    }
    return render(request, "useradmin/dashboard.html", context)


@login_required
@staff_member_required
def dashboard_products(request):
    if request.user.is_superuser:
        all_products = Product.objects.all().order_by("-id")
    else:
        vendor = get_user_vendor(request.user)
        all_products = Product.objects.filter(
            Q(vendor=vendor) | Q(user=request.user)
        ).order_by("-id")
    
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/dashboard-products.html", context)


@login_required
@staff_member_required
def dashboard_add_product(request):
    vendor = get_user_vendor(request.user)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            if vendor:
                new_form.vendor = vendor
            new_form.save()
            form.save_m2m()
            messages.success(request, "Product added successfully.")
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm()
    context = {
        'form': form
    }
    return render(request, "useradmin/dashboard-add-products.html", context)


@login_required
@staff_member_required
def dashboard_edit_product(request, pid):
    if request.user.is_superuser:
        product = get_object_or_404(Product, pid=pid)
    else:
        vendor = get_user_vendor(request.user)
        product = get_object_or_404(Product, Q(user=request.user) | Q(vendor=vendor), pid=pid)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            if not new_form.vendor:
                vendor = get_user_vendor(request.user)
                if vendor:
                    new_form.vendor = vendor
            new_form.save()
            form.save_m2m()
            messages.success(request, "Product updated successfully.")
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, "useradmin/dashboard-edit-products.html", context)


@login_required
@staff_member_required
@require_POST
def dashboard_delete_product(request, pid):
    if request.user.is_superuser:
        product = get_object_or_404(Product, pid=pid)
    else:
        vendor = get_user_vendor(request.user)
        product = get_object_or_404(Product, Q(user=request.user) | Q(vendor=vendor), pid=pid)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("useradmin:dashboard-products")


@login_required
@staff_member_required
def dashboard_orders(request):
    if request.user.is_superuser:
        orders = list(CartOrder.objects.all().order_by("-id"))
        for ord_obj in orders:
            ord_obj.display_total = ord_obj.price
            ord_obj.items_count = ord_obj.cartorderproducts_set.count()
    else:
        vendor = get_user_vendor(request.user)
        if not vendor:
            orders = []
        else:
            vendor_items = CartOrderProducts.objects.filter(
                Q(vendor=vendor) | Q(product__user=request.user)
            )
            orders_qs = CartOrder.objects.filter(
                cartorderproducts__in=vendor_items
            ).distinct().order_by("-id")
            orders = list(orders_qs)
            for ord_obj in orders:
                ord_vendor_items = vendor_items.filter(order=ord_obj)
                ord_obj.display_total = ord_vendor_items.aggregate(s=Sum('total'))['s'] or 0
                ord_obj.items_count = ord_vendor_items.count()

    context = {
        "orders": orders,
    }
    return render(request, "useradmin/dashboard-orders.html", context)


@login_required
@staff_member_required
def dashboard_order_detail(request, id):
    order = get_object_or_404(CartOrder, id=id)

    if request.user.is_superuser:
        order_items = CartOrderProducts.objects.filter(order=order)
        order_subtotal = order.price
    else:
        vendor = get_user_vendor(request.user)
        if not vendor:
            raise Http404("Vendor profile not found.")
        order_items = CartOrderProducts.objects.filter(
            Q(vendor=vendor) | Q(product__user=request.user),
            order=order
        )
        if not order_items.exists():
            raise Http404("You do not have permission to view this order.")
        order_subtotal = order_items.aggregate(s=Sum('total'))['s'] or 0

    address = Address.objects.filter(user=order.user, status=True).first()
    if not address:
        address = Address.objects.filter(user=order.user).first()

    context = {
        "order": order,
        "order_items": order_items,
        "order_subtotal": order_subtotal,
        "address": address,
    }
    return render(request, "useradmin/dashboard-order-detail.html", context)


@login_required
@staff_member_required
@require_POST
def dashboard_change_order_status(request, id):
    order = get_object_or_404(CartOrder, id=id)
    status = request.POST.get("status")
    if status:
        if request.user.is_superuser:
            order.product_status = status
            order.save()
            CartOrderProducts.objects.filter(order=order).update(product_status=status)
        else:
            vendor = get_user_vendor(request.user)
            if vendor:
                CartOrderProducts.objects.filter(
                    Q(vendor=vendor) | Q(product__user=request.user),
                    order=order
                ).update(product_status=status)
        messages.success(request, f"Order status updated to {status}.")
    return redirect("useradmin:dashboard-order-detail", id=id)


@login_required
@staff_member_required
def dashboard_settings(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None

    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Vendor Profile updated successfully.")
            return redirect("useradmin:dashboard-settings")
    else:
        form = VendorForm(instance=vendor)

    context = {
        'form': form,
        'vendor': vendor,
    }
    return render(request, "useradmin/dashboard-settings.html", context)