
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from requests import session
from taggit.models import Tag
from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist_model, Address
from site_settings.models import Slider, HomeBanner
from userauths.models import ContactUs, Profile
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required

import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth
from django.core import serializers
from django.contrib.auth.decorators import login_required

from decimal import Decimal

def safe_float(val):
    if val is None:
        return 0.0
    val_str = str(val).replace(',', '').replace('$', '').strip()
    if not val_str:
        return 0.0
    if val_str.count('.') > 1:
        parts = val_str.rsplit('.', 1)
        val_str = parts[0].replace('.', '') + '.' + parts[1]
    try:
        return float(val_str)
    except (ValueError, TypeError):
        return 0.0

def safe_decimal(val):
    return Decimal(f"{safe_float(val):.2f}")

def index(request):
    # bannanas = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True).order_by("-id")
    sliders = Slider.objects.all()
    home_banners = HomeBanner.objects.all()[:3]
    deals_of_the_day = Product.objects.filter(deal_of_the_day=True, product_status="published").order_by("-id")[:4]

    recently_added = Product.objects.filter(product_status="published").order_by("-date")[:3]
    top_selling = Product.objects.filter(product_status="published", is_top_selling=True).order_by("-id")[:3]
    trending_products = Product.objects.filter(product_status="published", is_trending=True).order_by("-id")[:3]
    top_rated = Product.objects.filter(product_status="published", is_top_rated=True).order_by("-id")[:3]

    context = {
        "products":products,
        "sliders":sliders,
        "home_banners":home_banners,
        "deals_of_the_day":deals_of_the_day,
        "recently_added":recently_added,
        "top_selling":top_selling,
        "trending_products":trending_products,
        "top_rated":top_rated,
    }

    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tags = Tag.objects.all().order_by("-id")[:6]

    context = {
        "products":products,
        "tags":tags,
    }

    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list__view(request, cid):

    category = Category.objects.get(cid=cid) # food, Cosmetics
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, "core/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published").order_by("-id")

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "core/vendor-detail.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product Review form
    review_form = ProductReviewForm()


    make_review = True 

    address = "Login To Continue"

    if request.user.is_authenticated:
        address = Address.objects.filter(status=True, user=request.user).first()
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False


    p_image = product.p_images.all()

    context = {
        "p": product,
        "address": address,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):

    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "core/tag.html", context)


@login_required
def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user 

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
       {
         'bool': True,
        'context': context,
        'average_reviews': average_reviews
       }
    )


def search_view(request):
    query = request.GET.get("q")
    
    if not query:
        return redirect("core:product-list")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")


    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() 
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct() 
    
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    p_id = str(request.GET.get('id', ''))
    title = request.GET.get('title', '')
    qty_val = request.GET.get('qty', 1)
    price_val = request.GET.get('price', '')
    image_val = request.GET.get('image', '')
    pid_val = request.GET.get('pid', '')

    try:
        qty = int(qty_val)
        if qty < 1:
            qty = 1
    except (ValueError, TypeError):
        qty = 1

    # Look up product in DB to ensure valid, correct data
    try:
        product = Product.objects.get(id=int(p_id))
        price_clean = f"{product.price:.2f}"
        title = product.title
        image_val = product.image.url if product.image else image_val
        pid_val = product.pid
    except Exception:
        price_clean = f"{safe_float(price_val):.2f}"

    cart_product = {
        p_id: {
            'title': title,
            'qty': qty,
            'price': price_clean,
            'image': image_val,
            'pid': pid_val,
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if p_id in cart_data:
            existing_qty = int(cart_data[p_id].get('qty', 0))
            cart_data[p_id]['qty'] = existing_qty + qty
            cart_data[p_id]['price'] = price_clean
            cart_data[p_id]['title'] = title
            cart_data[p_id]['image'] = image_val
            cart_data[p_id]['pid'] = pid_val
        else:
            cart_data.update(cart_product)
        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    request.session.modified = True
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session and len(request.session['cart_data_obj']) > 0:
        cart_data = request.session['cart_data_obj']
        for p_id, item in list(cart_data.items()):
            # Synchronize product data if missing
            try:
                product = Product.objects.get(id=int(p_id))
                item['price'] = f"{product.price:.2f}"
                if not item.get('title'):
                    item['title'] = product.title
                if not item.get('image') and product.image:
                    item['image'] = product.image.url
                if not item.get('pid'):
                    item['pid'] = product.pid
            except Exception:
                item['price'] = f"{safe_float(item.get('price', 0)):.2f}"

            try:
                qty = int(item.get('qty', 1))
                if qty < 1:
                    qty = 1
            except Exception:
                qty = 1
            item['qty'] = qty

            sub_total = qty * safe_float(item['price'])
            item['sub_total'] = sub_total
            cart_total_amount += sub_total

        request.session['cart_data_obj'] = cart_data
        request.session.modified = True
        return render(request, "core/cart.html", {
            "cart_data": cart_data, 
            'totalcartitems': len(cart_data), 
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET.get('id', ''))
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
    
    cart_total_amount = 0
    cart_data = request.session.get('cart_data_obj', {})
    if cart_data:
        for p_id, item in cart_data.items():
            try:
                product = Product.objects.get(id=int(p_id))
                item['price'] = f"{product.price:.2f}"
            except Exception:
                item['price'] = f"{safe_float(item.get('price', 0)):.2f}"
            try:
                qty = int(item.get('qty', 1))
            except Exception:
                qty = 1
            item['qty'] = qty
            sub_total = qty * safe_float(item['price'])
            item['sub_total'] = sub_total
            cart_total_amount += sub_total

    context = render_to_string("core/async/cart-list.html", {
        "cart_data": cart_data, 
        'totalcartitems': len(cart_data), 
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({"data": context, 'totalcartitems': len(cart_data)})


def update_cart(request):
    product_id = str(request.GET.get('id', ''))
    product_qty = request.GET.get('qty', 1)

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            try:
                qty = int(product_qty)
                if qty < 1:
                    qty = 1
            except Exception:
                qty = 1
            cart_data[product_id]['qty'] = qty
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
    
    cart_total_amount = 0
    cart_data = request.session.get('cart_data_obj', {})
    if cart_data:
        for p_id, item in cart_data.items():
            try:
                product = Product.objects.get(id=int(p_id))
                item['price'] = f"{product.price:.2f}"
            except Exception:
                item['price'] = f"{safe_float(item.get('price', 0)):.2f}"
            try:
                qty = int(item.get('qty', 1))
            except Exception:
                qty = 1
            item['qty'] = qty
            sub_total = qty * safe_float(item['price'])
            item['sub_total'] = sub_total
            cart_total_amount += sub_total

    context = render_to_string("core/async/cart-list.html", {
        "cart_data": cart_data, 
        'totalcartitems': len(cart_data), 
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({"data": context, 'totalcartitems': len(cart_data)})


@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    # Checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session and len(request.session['cart_data_obj']) > 0:
        cart_data = request.session['cart_data_obj']

        # Ensure all cart items have valid data from DB
        for p_id, item in list(cart_data.items()):
            try:
                product = Product.objects.get(id=int(p_id))
                item['price'] = f"{product.price:.2f}"
                if not item.get('title'):
                    item['title'] = product.title
                if not item.get('image') and product.image:
                    item['image'] = product.image.url
                if not item.get('pid'):
                    item['pid'] = product.pid
            except Exception:
                item['price'] = f"{safe_float(item.get('price', 0)):.2f}"

            try:
                qty = int(item.get('qty', 1))
                if qty < 1:
                    qty = 1
            except Exception:
                qty = 1
            item['qty'] = qty

            sub_total = qty * safe_float(item['price'])
            item['sub_total'] = sub_total
            total_amount += sub_total

        cart_total_amount = total_amount
        request.session['cart_data_obj'] = cart_data
        request.session.modified = True

        order_price_dec = safe_decimal(total_amount)

        if request.method == "POST":
            # Handle Cash on Delivery / Direct Bank Transfer order placement
            payment_option = request.POST.get('payment_option', 'cod')
            billing_address_text = request.POST.get('billing_address', '').strip()
            mobile_text = request.POST.get('lname', '').strip() or request.POST.get('mobile', '').strip()

            if billing_address_text:
                try:
                    Address.objects.filter(user=request.user).update(status=False)
                    Address.objects.create(user=request.user, address=billing_address_text, mobile=mobile_text, status=True)
                except Exception:
                    pass

            order = CartOrder.objects.create(
                user=request.user,
                price=order_price_dec,
                paid_status=False,
                product_status="processing"
            )
    
            for p_id, item in cart_data.items():
                item_price_dec = safe_decimal(item['price'])
                item_qty = int(item['qty'])
                item_total_dec = safe_decimal(item_qty * safe_float(item['price']))

                item_product = None
                try:
                    item_product = Product.objects.filter(id=int(p_id)).first()
                except (ValueError, TypeError):
                    item_product = Product.objects.filter(pid=p_id).first()
                if not item_product and item.get('title'):
                    item_product = Product.objects.filter(title=item.get('title')).first()
                
                item_vendor = item_product.vendor if (item_product and item_product.vendor) else (Vendor.objects.filter(user=item_product.user).first() if (item_product and item_product.user) else None)

                CartOrderProducts.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),
                    item=item.get('title', 'Product'),
                    image=item.get('image', ''),
                    qty=item_qty,
                    price=item_price_dec,
                    total=item_total_dec,
                    vendor=item_vendor,
                    product=item_product
                )

            # Clear session cart for COD / Bank transfer orders
            del request.session['cart_data_obj']
            request.session.modified = True

            messages.success(request, "Your order has been placed successfully!")
            return render(request, 'core/payment-completed.html', {
                'order': order,
                'cart_data': cart_data,
                'totalcartitems': len(cart_data),
                'cart_total_amount': cart_total_amount
            })
        else:
            order = CartOrder.objects.filter(user=request.user, paid_status=False).order_by('-id').first()
            if not order:
                order = CartOrder.objects.create(
                    user=request.user,
                    paid_status=False,
                    price=order_price_dec
                )
            else:
                order.price = order_price_dec
                order.save()
            
            # Clear old products for this unpaid order to prevent duplicates if cart changed
            CartOrderProducts.objects.filter(order=order).delete()
            
            for p_id, item in cart_data.items():
                item_price_dec = safe_decimal(item['price'])
                item_qty = int(item['qty'])
                item_total_dec = safe_decimal(item_qty * safe_float(item['price']))

                item_product = None
                try:
                    item_product = Product.objects.filter(id=int(p_id)).first()
                except (ValueError, TypeError):
                    item_product = Product.objects.filter(pid=p_id).first()
                if not item_product and item.get('title'):
                    item_product = Product.objects.filter(title=item.get('title')).first()
                
                item_vendor = item_product.vendor if (item_product and item_product.vendor) else (Vendor.objects.filter(user=item_product.user).first() if (item_product and item_product.user) else None)

                CartOrderProducts.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),
                    item=item.get('title', 'Product'),
                    image=item.get('image', ''),
                    qty=item_qty,
                    price=item_price_dec,
                    total=item_total_dec,
                    vendor=item_vendor,
                    product=item_product
                )

        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart_total_amount,
            'item_name': "Order-Item-No-" + str(order.id),
            'invoice': "INVOICE_NO-" + str(order.id),
            'currency_code': "USD",
            'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
            'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
            'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
        }

        paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

        try:
            active_address = Address.objects.get(user=request.user, status=True)
        except Exception:
            active_address = None

        return render(request, "core/checkout.html", {"cart_data": cart_data, 'totalcartitems': len(cart_data), 'cart_total_amount': cart_total_amount, 'paypal_payment_button': paypal_payment_button, "active_address": active_address})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")


@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    recent_order = CartOrder.objects.filter(user=request.user).order_by('-id').first()
    if 'cart_data_obj' in request.session and len(request.session['cart_data_obj']) > 0:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            try:
                product = Product.objects.get(id=int(p_id))
                item['price'] = f"{product.price:.2f}"
            except Exception:
                item['price'] = f"{safe_float(item.get('price', 0)):.2f}"
            qty = int(item.get('qty', 1))
            sub_total = qty * safe_float(item['price'])
            item['sub_total'] = sub_total
            cart_total_amount += sub_total
        
        # Mark recent order as paid
        if recent_order and not recent_order.paid_status:
            recent_order.paid_status = True
            recent_order.save()

        del request.session['cart_data_obj']
        request.session.modified = True
        return render(request, 'core/payment-completed.html', {
            'order': recent_order,
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        })
    elif recent_order:
        order_items = CartOrderProducts.objects.filter(order=recent_order)
        cart_data = {}
        for item in order_items:
            cart_data[str(item.id)] = {
                'title': item.item,
                'price': f"{item.price:.2f}",
                'qty': item.qty,
                'sub_total': item.total,
                'image': item.image
            }
        return render(request, 'core/payment-completed.html', {
            'order': recent_order,
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': recent_order.price
        })
    return render(request, 'core/payment-completed.html', {'cart_data': {}, 'totalcartitems': 0, 'cart_total_amount': 0})

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)


    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:dashboard")
    
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if not user_profile.full_name:
        if request.user.first_name or request.user.last_name:
            user_profile.full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        elif request.user.username:
            user_profile.full_name = request.user.username.title()
        user_profile.save()

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)

    
    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)


@login_required
def make_address_default(request):
    id = request.GET['id']
    Address.objects.filter(user=request.user).update(status=False)
    Address.objects.filter(id=id, user=request.user).update(status=True)
    return JsonResponse({"boolean": True})

@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.filter(user=request.user)
    context = {
        "w":wishlist
    }
    return render(request, "core/wishlist.html", context)


    # w

@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)


# def remove_wishlist(request):
#     pid = request.GET['id']
#     wishlist = wishlist_model.objects.filter(user=request.user).values()

#     product = wishlist_model.objects.get(id=pid)
#     h = product.delete()

#     context = {
#         "bool": True,
#         "wishlist":wishlist
#     }
#     t = render_to_string("core/async/wishlist-list.html", context)
#     return JsonResponse({"data": t, "w":wishlist})

@login_required
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_d = wishlist_model.objects.get(id=pid)
    delete_product = wishlist_d.delete()
    
    context = {
        "bool":True,
        "w":wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({'data':t,'w':wishlist_json})





# Other Pages 
def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})


def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def terms_of_service(request):
    return render(request, "core/terms_of_service.html")


