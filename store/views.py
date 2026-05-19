from django.shortcuts import render, redirect, get_object_or_404
from .models import Fragrance, SliderImage, About,  Variant, Order, OrderItem
import urllib.parse


# ------------------------
# HOME
# ------------------------
def home(request):
    sliders = SliderImage.objects.filter(is_active=True)

    # Get one product per category safely
    him = Fragrance.objects.filter(category='him', is_active=True).first()
    her = Fragrance.objects.filter(category='her', is_active=True).first()
    oud = Fragrance.objects.filter(category='oud', is_active=True).first()
    unisex = Fragrance.objects.filter(category='unisex', is_active=True).first()

    # Build structured products list
    products = [
        {"label": "For Him", "product": him},
        {"label": "For Her", "product": her},
        {"label": "Unisex", "product": unisex},
        {"label": "Oud", "product": oud},
    ]

    # Remove empty products safely
    products = [p for p in products if p["product"]]

    about = About.objects.first()

    return render(request, 'store/home.html', {
        'sliders': sliders,
        'products': products,
        'about': about,
    })
    
def category_page(request, category):
    variants_100 = Variant.objects.filter(
        fragrance__category=category,
        size=100,
        is_active=True
    )

    variants_30 = Variant.objects.filter(
        fragrance__category=category,
        size=30,
        is_active=True
    )

    # ADD SAVE AMOUNT HERE (IMPORTANT)
    for v in list(variants_100) + list(variants_30):
        if v.mrp and v.mrp > v.selling_price:
            v.save_amount = v.mrp - v.selling_price
        else:
            v.save_amount = 0

    return render(request, 'store/category.html', {
        'variants_100': variants_100,
        'variants_30': variants_30,
        'title': category
    })
# ------------------------
# CATEGORY PAGES
# ------------------------
def him(request):
    fragrances = Fragrance.objects.filter(category='him')

    variants_100 = Variant.objects.filter(fragrance__in=fragrances, size='100', is_active=True)
    variants_30 = Variant.objects.filter(fragrance__in=fragrances, size='30', is_active=True)

    return render(request, 'store/category.html', {
        'title': 'Fragrances for Him',
        'variants_100': variants_100,
        'variants_30': variants_30,
    })


def her(request):
    fragrances = Fragrance.objects.filter(category='her')

    variants_100 = Variant.objects.filter(fragrance__in=fragrances, size='100', is_active=True)
    variants_30 = Variant.objects.filter(fragrance__in=fragrances, size='30', is_active=True)

    return render(request, 'store/category.html', {
        'title': 'Fragrances for Her',
        'variants_100': variants_100,
        'variants_30': variants_30,
    })


def unisex(request):
    fragrances = Fragrance.objects.filter(category='unisex')

    variants_100 = Variant.objects.filter(fragrance__in=fragrances, size='100', is_active=True)
    variants_30 = Variant.objects.filter(fragrance__in=fragrances, size='30', is_active=True)

    return render(request, 'store/category.html', {
        'title': 'Unisex Collection',
        'variants_100': variants_100,
        'variants_30': variants_30,
    })


def oud(request):
    fragrances = Fragrance.objects.filter(category='oud')

    variants_100 = Variant.objects.filter(fragrance__in=fragrances, size='100', is_active=True)
    variants_30 = Variant.objects.filter(fragrance__in=fragrances, size='30', is_active=True)

    return render(request, 'store/category.html', {
        'title': 'Oud Collection',
        'variants_100': variants_100,
        'variants_30': variants_30,
    })


# ------------------------
# FRAGRANCE VIEWS
# ------------------------
def fragrance_list(request):
    fragrances = Fragrance.objects.filter(is_active=True)

    for fragrance in fragrances:
        variant = fragrance.variants.first()
        fragrance.main_variant = variant

        if variant and variant.mrp and variant.mrp > variant.selling_price:
            variant.save_amount = variant.mrp - variant.selling_price
        else:
            variant.save_amount = 0

    return render(request, 'store/fragrance_list.html', {
        'fragrances': fragrances
    })

def fragrance_detail(request, pk):
    fragrance = get_object_or_404(Fragrance, pk=pk, is_active=True)

    variants_qs = fragrance.variants.filter(is_active=True)

    # attach save amount to each variant
    variants = []

    for v in variants_qs:
        v.save_amount = v.mrp - v.selling_price
        variants.append(v)

    return render(request, 'store/fragrance_detail.html', {
        'fragrance': fragrance,
        'variants': variants
    })


# ------------------------
# CART (SESSION BASED)
# ------------------------
def add_to_cart(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id, is_active=True)

    cart = request.session.get('cart', {})
    item_id = str(variant.id)

    if item_id in cart:
        cart[item_id]['quantity'] += 1
    else:
        cart[item_id] = {
            'variant_id': variant.id,
            'name': variant.fragrance.name,
            'size': variant.size,
            'mrp': float(variant.mrp),
            'price': float(variant.selling_price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def increase_quantity(request, variant_id):
    cart = request.session.get('cart', {})
    item_id = str(variant_id)

    if item_id in cart:
        cart[item_id]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('view_cart')


def decrease_quantity(request, variant_id):
    cart = request.session.get('cart', {})
    item_id = str(variant_id)

    if item_id in cart:
        cart[item_id]['quantity'] -= 1
        if cart[item_id]['quantity'] <= 0:
            del cart[item_id]

    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, variant_id):
    cart = request.session.get('cart', {})
    item_id = str(variant_id)

    if item_id in cart:
        del cart[item_id]

    request.session['cart'] = cart
    return redirect('view_cart')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})

    total = 0
    mrp_total = 0

    for item in cart.values():
        qty = item['quantity']
        total += item['price'] * qty
        mrp_total += item['mrp'] * qty

    savings = mrp_total - total

    return render(request, 'store/cart.html', {
        'cart': cart,
        'total': total,
        'mrp_total': mrp_total,
        'savings': savings,
    })


# ------------------------
# CHECKOUT
# ------------------------
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('fragrance_list')

    total = 0

    for item in cart.values():
        total += item['price'] * item['quantity']

    if request.method == 'POST':

        # store user data temporarily
        request.session['order_data'] = {
            'full_name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'payment_method': request.POST.get('payment_method'),
            'total': total,
        }

        payment_method = request.POST.get('payment_method')

        # COD → directly place order
        if payment_method == 'cod':
            return redirect('place_order')

        # ONLINE → show QR page
        return redirect('online_payment')

    return render(request, 'store/checkout.html', {
        'total': total
    })
# ------------------------
# ORDER SUCCESS
# ------------------------
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(request, 'store/success.html', {
        'order': order
    })

def online_payment(request):
    about = About.objects.first()

    qr = None
    if about and about.qr_code:
        qr = about.qr_code.url   # ✅ THIS IS IMPORTANT

    return render(request, 'store/online_payment.html', {
        'qr': qr
    })
    
def place_order(request):
    cart = request.session.get('cart', {})
    order_data = request.session.get('order_data')

    if not cart or not order_data:
        return redirect('checkout')

    total = order_data['total']

    order = Order.objects.create(
        full_name=order_data['full_name'],
        phone=order_data['phone'],
        email=order_data['email'],
        address=order_data['address'],
        total_amount=total,
        payment_method=order_data['payment_method'],
        status='confirmed'
    )

    for item in cart.values():
        OrderItem.objects.create(
            order=order,
            product_name=item['name'],
            size=item['size'],
            price=item['price'],
            quantity=item['quantity']
        )

    request.session['cart'] = {}
    request.session.pop('order_data', None)

    return redirect('order_success', order_id=order.id)