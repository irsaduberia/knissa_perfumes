from .models import SiteSettings, SliderImage

def global_data(request):
    return {
        'site_settings': SiteSettings.objects.first(),
        'sliders': SliderImage.objects.filter(is_active=True)
    }

def cart_count(request):
    cart = request.session.get('cart', {})

    count = sum(item.get('quantity', 0) for item in cart.values())

    return {
        'cart_count': count
    }